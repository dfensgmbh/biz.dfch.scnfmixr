# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module state_machine."""

from __future__ import annotations
from enum import Enum, auto
import threading
from typing import cast

from biz.dfch.logging import log
from biz.dfch.asyn import ConcurrentDoubleSideQueueT

from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..system import MessageQueue
from ..ui import UserInteractionAudio
from ..app import ApplicationContext
from .fsm import ExecutionContext, Fsm, StateBase


from .states import FinalState

from .states import System
from .transitions import ReturningTrue
from .transitions import SettingDate, StoppingSystem, DisconnectingStorage

from .states import SelectLanguage
from .transitions import SelectingEnglish, SelectingGerman, SelectingFrench, SelectingItalian \
    # pylint: disable=C0301  # noqa: E501

from .states import InitialiseLcl
from .transitions import DetectingLcl, SkippingLcl

from .states import InitialiseEx1
from .transitions import DetectingEx1, SkippingEx1

from .states import InitialiseEx2
from .transitions import DetectingEx2, SkippingEx2

from .states import InitialiseHi1
from .transitions import DetectingHi1, SkippingHi1

from .states import InitialiseRc1
from .transitions import DetectingRc1, SkippingRc1, CleaningRc1, MountingRc1, UnmountingRc1 \
    # pylint: disable=C0301  # noqa: E501

from .states import InitialiseRc2
from .transitions import DetectingRc2, SkippingRc2, CleaningRc2, MountingRc2, UnmountingRc2 \
    # pylint: disable=C0301  # noqa: E501

from .states import SetDate, SetTime, SetName
from .transitions import ProcessingDigit

from .states import InitialiseAudio
from .transitions import InitialisingAudio

from .states import Main
from .transitions import StartingRecording

from .states import OnRecord
from .transitions import StoppingRecording, SettingCuePoint, TogglingMute, ShowingStatus \
    # pylint: disable=C0301  # noqa: E501

from .states import Playback
from .transitions import (
    SelectingPause,
    SeekingPrevious,
    SeekingNext,
    JumpingClipStart,
    JumpingClipEnd,
    JumpingClipPrevious,
    JumpingClipNext,
    JumpingCuePrevious,
    JumpingCueNext,
    LeavingPlayback,
)


class State(Enum):
    """Names for state menu map."""
    INIT_LCL = auto()
    INIT_EX1 = auto()
    INIT_EX2 = auto()
    INIT_HI1 = auto()
    INIT_HI2 = auto()
    INIT_HI3 = auto()
    INIT_RC1 = auto()
    INIT_RC2 = auto()
    LANGUAGE = auto()
    SET_DATE = auto()
    SET_TIME = auto()
    SET_NAME = auto()
    INIT_AUDIO = auto()
    SYSTEM = auto()
    MAIN = auto()
    ON_RECORD = auto()
    PLAYBACK = auto()
    FINAL = auto()


class StateMachine:
    """StateMachine of the application."""

    WAIT_INTERVAL_MS: int = 250
    _BLOCK_INTERVAL_MS: int = 5000

    _ui: UserInteractionAudio
    _app_ctx: ApplicationContext
    _signal_worker: threading.Event
    _event_queue: ConcurrentDoubleSideQueueT[str]
    _messsage_queue: MessageQueue
    _do_cancel_worker: bool
    _thread: threading.Thread
    _ctx: ExecutionContext
    _fsm: Fsm
    _menu: dict[State, StateBase]

    def __init__(self):

        # DFTODO - adjust to something dynamic.
        self._ui = UserInteractionAudio("system")

        self._app_ctx = ApplicationContext.Factory.get()
        self._signal_worker = threading.Event()
        self._event_queue = ConcurrentDoubleSideQueueT[str]()
        self._messsage_queue = MessageQueue.Factory.get()
        self._do_cancel_worker = False
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._ctx = None
        self._fsm = None
        self._messsage_queue.register(self._on_message, lambda e: isinstance(
            e,
            (SystemMessage.InputEvent, SystemMessage.Shutdown)))
        self._menu = {}

    def start(self) -> None:
        "Starts the state machine."

        self.initialise()
        self._thread.start()

    @property
    def is_started(self) -> bool:
        """Determines whether the state machine is started or not.

        Returns:
            bool: True, if the state machine is started; false otherwise.
        """
        return self._fsm.is_started

    def _on_message(self, message: MessageBase) -> None:
        """Process: SystemMessage.InputEvent"""

        if not isinstance(
                message,
                (SystemMessage.InputEvent, SystemMessage.Shutdown)):
            return

        if isinstance(message, SystemMessage.Shutdown):
            self._do_cancel_worker = True
            self._signal_worker.set()
            return

        event = cast(SystemMessage.InputEvent, message)
        log.debug("Received message with input event: '%s' [%s]",
                  event.value,
                  event.name)

        if isinstance(event, SystemMessage.InputEventClear):
            self._event_queue.clear()
            self._event_queue.enqueue_first(event.value)

        elif isinstance(event, SystemMessage.InputEventFirst):
            self._event_queue.enqueue_first(event.value)

        elif isinstance(event, SystemMessage.InputEvent):
            self._event_queue.enqueue(event.value)

        else:
            log.warning("Unsupported type: '%s'.", event.name)
            return

        self._signal_worker.set()

    def _worker(self) -> None:
        """The worker thread that dequeues and processes state machine events.

        Args:
            None:

        Returns:
            None:
        """

        log.debug("Initialising worker ...")

        log.info("Initialising worker OK.")

        while True:

            try:

                log.debug("Waiting for event ...")

                result = False

                if self._event_queue.is_empty():

                    result = self._signal_worker.wait(
                        self._BLOCK_INTERVAL_MS / 1000)
                    self._signal_worker.clear()

                    if self._do_cancel_worker:

                        log.debug("Stopping worker ...")
                        break

                    if not result:
                        continue

                event = self._event_queue.dequeue()
                if event is None:
                    continue

                log.debug("Invocation of event '%s' ... [is_started=%s]",
                          event,
                          self._fsm.is_started)

                try:

                    result = self._fsm.invoke(event)

                    if result:
                        log.info(
                            "Invocation of event '%s' OK. [is_started=%s]",  # noqa: E501  # pylint: disable=C0301
                            event,
                            self._fsm.is_started)
                    else:
                        log.warning(
                            "Invocation of event '%s' FAILED. [is_started=%s]",
                            event,
                            self._fsm.is_started)

                except Exception as ex:
                    log.error(
                        "Invocation of event '%s' FAILED. [is_started=%s] [%s]",
                        event,
                        self._fsm.is_started,
                        ex,
                        exc_info=True)
                    raise

            except Exception as ex:  # pylint: disable=W0718

                log.error(
                    "An exception occurred inside the worker thread: '%s'.",
                    ex,
                    exc_info=True)

        log.info("Stopping worker OK.")

    def initialise(self) -> None:
        """Initialises the state machine."""

        log.info("Initialising state machine ...")

        # Define States
        menu = self._menu

        assert State.INIT_LCL not in menu
        menu[State.INIT_LCL] = InitialiseLcl()

        assert State.INIT_HI1 not in menu
        menu[State.INIT_HI1] = InitialiseHi1()

        assert State.INIT_EX1 not in menu
        menu[State.INIT_EX1] = InitialiseEx1()

        assert State.INIT_EX2 not in menu
        menu[State.INIT_EX2] = InitialiseEx2()

        assert State.LANGUAGE not in menu
        menu[State.LANGUAGE] = SelectLanguage()

        assert State.INIT_RC1 not in menu
        menu[State.INIT_RC1] = InitialiseRc1()

        assert State.INIT_RC2 not in menu
        menu[State.INIT_RC2] = InitialiseRc2()

        assert State.SET_DATE not in menu
        menu[State.SET_DATE] = SetDate()

        assert State.SET_TIME not in menu
        menu[State.SET_TIME] = SetTime()

        assert State.SET_NAME not in menu
        menu[State.SET_NAME] = SetName()

        assert State.MAIN not in menu
        menu[State.MAIN] = Main()

        assert State.ON_RECORD not in menu
        menu[State.ON_RECORD] = OnRecord()

        assert State.INIT_AUDIO not in menu
        menu[State.INIT_AUDIO] = InitialiseAudio()

        assert State.PLAYBACK not in menu
        menu[State.PLAYBACK] = Playback()

        assert State.SYSTEM not in menu
        menu[State.SYSTEM] = System()

        assert State.FINAL not in menu
        menu[State.FINAL] = FinalState()

        # Define Transitions
        current: FinalState = menu[State.FINAL]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(ReturningTrue(current.Event.MENU,
                                          current))
        )
        current: System = menu[State.SYSTEM]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(ReturningTrue(
                current.Event.SELECT_MAIN,
                menu[State.MAIN]))
            .add_transition(ReturningTrue(
                current.Event.SELECT_LANGUAGE,
                menu[State.LANGUAGE]))
            .add_transition(SettingDate(
                current.Event.SET_DATE,
                menu[State.SET_DATE]))
            .add_transition(ReturningTrue(
                current.Event.SET_TIME,
                menu[State.SET_TIME]))
            .add_transition(ReturningTrue(
                current.Event.SET_NAME,
                menu[State.SET_NAME]))
            .add_transition(ReturningTrue(
                current.Event.DETECT_STORAGE,
                menu[State.INIT_RC1]))
            .add_transition(DisconnectingStorage(
                current.Event.DISCONNECT_STORAGE,
                current))
            .add_transition(StoppingSystem(
                current.Event.STOP_SYSTEM,
                menu[State.FINAL]))
        )
        current: OnRecord = menu[State.ON_RECORD]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(StoppingRecording(
                current.Event.STOP_RECORDING,
                menu[State.MAIN]))
            .add_transition(SettingCuePoint(
                current.Event.SET_CUE,
                current))
            .add_transition(TogglingMute(
                current.Event.TOGGLE_MUTE,
                current))
            .add_transition(ShowingStatus(
                current.Event.SHOW_STATUS,
                current))
        )
        current: Main = menu[State.MAIN]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(ReturningTrue(
                current.Event.MENU,
                menu[State.SYSTEM]))
            .add_transition(StartingRecording(
                current.Event.START_RECORDING,
                menu[State.ON_RECORD]))
            .add_transition(ReturningTrue(
                current.Event.START_PLAYBACK,
                menu[State.PLAYBACK]))
            .add_transition(StoppingSystem(
                current.Event.STOP_SYSTEM,
                menu[State.FINAL]))
        )
        current: InitialiseAudio = menu[State.INIT_AUDIO]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(InitialisingAudio(current.Event.INIT_AUDIO,
                                              menu[State.MAIN]))
            .add_transition(InitialisingAudio(current.Event.SKIP_AUDIO,
                                              menu[State.SYSTEM]))
        )
        current: SetName = menu[State.SET_NAME]
        (
            current
            .add_transition(ProcessingDigit(current.Event.DIGIT_0, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_1, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_2, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_3, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_4, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_5, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_6, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_7, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_8, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_9, current))
            .add_transition(ProcessingDigit(current.Event.BACK_SPACE, current))
            .add_transition(ProcessingDigit(current.Event.ENTER, current))
            .add_transition(ReturningTrue(
                current.Event.JUMP_NEXT,
                menu[State.INIT_AUDIO]))
        )
        current: SetTime = menu[State.SET_TIME]
        (
            current
            .add_transition(ProcessingDigit(current.Event.DIGIT_0, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_1, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_2, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_3, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_4, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_5, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_6, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_7, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_8, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_9, current))
            .add_transition(ProcessingDigit(current.Event.BACK_SPACE, current))
            .add_transition(ProcessingDigit(current.Event.ENTER, current))
            .add_transition(ReturningTrue(
                current.Event.JUMP_NEXT,
                menu[State.SET_NAME]))
        )
        current: SetDate = menu[State.SET_DATE]
        (
            current
            .add_transition(ProcessingDigit(current.Event.DIGIT_0, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_1, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_2, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_3, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_4, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_5, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_6, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_7, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_8, current))
            .add_transition(ProcessingDigit(current.Event.DIGIT_9, current))
            .add_transition(ProcessingDigit(current.Event.BACK_SPACE, current))
            .add_transition(ProcessingDigit(current.Event.ENTER, current))
            .add_transition(ReturningTrue(
                current.Event.JUMP_NEXT,
                menu[State.SET_TIME]))
        )
        current: InitialiseRc2 = menu[State.INIT_RC2]
        (
            current
            .add_transition(ReturningTrue(current.Event.HELP,
                                          current))
            .add_transition(ReturningTrue(
                current.Event.MENU,
                menu[State.SYSTEM]))
            .add_transition(DetectingRc2(
                current.Event.DETECT_DEVICE,
                menu[State.SET_DATE]))
            .add_transition(SkippingRc2(
                current.Event.SKIP_DEVICE,
                menu[State.SET_DATE]))
            .add_transition(CleaningRc2(
                current.Event.CLEAN_DEVICE,
                current))
            .add_transition(MountingRc2(
                current.Event.MOUNT_DEVICE,
                current))
            .add_transition(UnmountingRc2(
                current.Event.UNMOUNT_DEVICE,
                current))
        )
        current: InitialiseRc1 = menu[State.INIT_RC1]
        (
            current
            .add_transition(ReturningTrue(current.Event.HELP,
                                          current))
            .add_transition(ReturningTrue(current.Event.MENU,
                                          menu[State.SYSTEM]))
            .add_transition(DetectingRc1(current.Event.DETECT_DEVICE,
                                         menu[State.INIT_RC2]))
            .add_transition(SkippingRc1(current.Event.SKIP_DEVICE,
                                        menu[State.INIT_RC2]))
            .add_transition(CleaningRc1(current.Event.CLEAN_DEVICE,
                                        current))
            .add_transition(MountingRc1(current.Event.MOUNT_DEVICE,
                                        current))
            .add_transition(UnmountingRc1(current.Event.UNMOUNT_DEVICE,
                                          current))
        )
        current: InitialiseEx2 = menu[State.INIT_EX2]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(DetectingEx2(
                current.Event.DETECT_DEVICE,

                menu[State.INIT_RC1]))
            .add_transition(SkippingEx2(
                current.Event.SKIP_DEVICE,
                menu[State.INIT_RC1]))
        )
        current: InitialiseEx1 = menu[State.INIT_EX1]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(DetectingEx1(
                current.Event.DETECT_DEVICE,
                menu[State.INIT_EX2]))
            .add_transition(SkippingEx1(
                current.Event.SKIP_DEVICE,
                menu[State.INIT_EX2]))
        )
        current: SelectLanguage = menu[State.LANGUAGE]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(ReturningTrue(
                current.Event.MENU,
                menu[State.SYSTEM]))
            .add_transition(SelectingEnglish(
                current.Event.SELECT_ENGLISH,
                menu[State.INIT_EX1]))
            .add_transition(SelectingGerman(
                current.Event.SELECT_GERMAN,
                menu[State.INIT_EX1]))
            .add_transition(SelectingFrench(
                current.Event.SELECT_FRENCH,
                menu[State.INIT_EX1]))
            .add_transition(SelectingItalian(
                current.Event.SELECT_ITALIAN,
                menu[State.INIT_EX1]))
        )
        current: InitialiseHi1 = menu[State.INIT_HI1]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(DetectingHi1(
                current.Event.DETECT_DEVICE,
                menu[State.LANGUAGE]))
            .add_transition(SkippingHi1(
                current.Event.SKIP_DEVICE,
                menu[State.LANGUAGE]))
        )
        current: InitialiseLcl = menu[State.INIT_LCL]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(ReturningTrue(
                current.Event.MENU,
                menu[State.SYSTEM]))
            .add_transition(DetectingLcl(
                current.Event.DETECT_DEVICE,
                menu[State.INIT_HI1]))
            .add_transition(SkippingLcl(
                current.Event.SKIP_DEVICE,
                menu[State.INIT_HI1]))
        )
        current: Playback = menu[State.PLAYBACK]
        (
            current
            .add_transition(ReturningTrue(
                current.Event.HELP,
                current))
            .add_transition(LeavingPlayback(
                current.Event.MENU,
                menu[State.MAIN]))
            .add_transition(SelectingPause(
                current.Event.PAUSE_RESUME,
                current))
            .add_transition(SeekingPrevious(
                current.Event.SEEK_PREVIOUS,
                current))
            .add_transition(SeekingNext(
                current.Event.SEEK_NEXT,
                current))
            .add_transition(JumpingClipStart(
                current.Event.JUMP_CLIP_START,
                current))
            .add_transition(JumpingClipEnd(
                current.Event.JUMP_CLIP_END,
                current))
            .add_transition(JumpingClipPrevious(
                current.Event.JUMP_CLIP_PREVIOUS,
                current))
            .add_transition(JumpingClipNext(
                current.Event.JUMP_CLIP_NEXT,
                current))
            .add_transition(JumpingCuePrevious(
                current.Event.JUMP_CUE_PREVIOUS,
                current))
            .add_transition(JumpingCueNext(
                current.Event.JUMP_CUE_NEXT,
                current))
        )

        self._ctx = ExecutionContext(None, None, events=self._messsage_queue)

        self._fsm = Fsm(initial_state=menu[State.INIT_LCL], ctx=self._ctx)
        self._fsm.start()

        # for line in self._fsm.visualise():
        #     log.debug(line)

        log.info("Initialising state machine OK.")
