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
import queue
import threading
import time

from biz.dfch.logging import log
from biz.dfch.asyn import ConcurrentQueueT

from ..ui import UserInteractionAudio
from ..app import ApplicationContext
from .fsm import ExecutionContext, Fsm


from .states import FinalState

from .states import SystemMenu
from .transitions import ReturningTrue

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

# from .states import InitialiseHi2
# from .transitions import DetectingHi2, SkippingHi2

# from .states import InitialiseHi3
# from .transitions import DetectingHi3, SkippingHi3

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

from .states import Record
from .transitions import StartingRecording, SettingDate, StoppingSystem, MountingStorage, DisconnectingStorage \
    # pylint: disable=C0301  # noqa: E501

from .states import OnRecord
from .transitions import StoppingRecording, SettingCuePoint, TogglingMute, ShowingStatus \
    # pylint: disable=C0301  # noqa: E501


class StateMachine:
    """StateMachine of the application."""

    WAIT_INTERVAL_MS: int = 250
    BLOCK_INTERVAL_MS: int = 250

    _app_ctx: ApplicationContext
    _queue: ConcurrentQueueT[str]
    _do_cancel_worker: threading.Event
    _thread: threading.Thread
    _ctx: ExecutionContext
    _fsm: Fsm

    def __init__(self):

        self._app_ctx = ApplicationContext.Factory.get()
        self._queue: ConcurrentQueueT[str] = ConcurrentQueueT(str, True)
        self._do_cancel_worker = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._ctx = None
        self._fsm = None

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

    def _worker(self) -> None:
        """The worker thread that dequeues and processes state machine events.

        Args:
            None:

        Returns:
            None:
        """

        log.debug("Starting worker ...")

        message_counter: int = 0
        while True:
            message_counter += 1

            try:
                if self._do_cancel_worker.is_set():

                    log.info("Exiting worker ...")
                    break

                if 0 == message_counter:
                    message_counter = 0
                    log.debug("Trying to dequeue item ...")

                event = self._queue.dequeue(self.BLOCK_INTERVAL_MS)

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

                except Exception:
                    log.error(
                        "Invocation of event '%s' FAILED. [is_started=%s]",
                        event,
                        self._fsm.is_started)
                    raise

            # Upon empty queue, just continue and try again.
            except queue.Empty:
                # log.debug(
                #     "Queue empty. Sleeping [%sms] ...",
                #     self.WAIT_INTERVAL_MS)
                pass

            # Upon timeout, just continue and try again.
            except TimeoutError:
                pass

            except Exception as ex:  # pylint: disable=W0718

                log.error(
                    "An exception occurred inside the worker thread: '%s'.",
                    ex,
                    exc_info=True)

            finally:
                time.sleep(self.WAIT_INTERVAL_MS/1000)

        log.debug("Stopping worker.")

    def initialise(self) -> None:
        """Initialises the state machine."""

        log.info("Initialising state machine ...")

        # Define States
        initialise_lcl = InitialiseLcl()
        initialise_hi1 = InitialiseHi1()
        select_language = SelectLanguage()
        initialise_ex1 = InitialiseEx1()
        initialise_ex2 = InitialiseEx2()
        initialise_rc1 = InitialiseRc1()
        initialise_rc2 = InitialiseRc2()
        set_date = SetDate()
        set_time = SetTime()
        set_name = SetName()
        record_menu = Record()
        initialise_audio = InitialiseAudio()
        onrecord_menu = OnRecord()
        system_menu = SystemMenu()
        final_state = FinalState()

        # Define Transitions
        (
            final_state
            .add_transition(ReturningTrue(FinalState.Event.MENU,
                                          final_state))
        )
        (
            system_menu
            .add_transition(ReturningTrue(SystemMenu.Event.MENU,
                                          system_menu))
            .add_transition(ReturningTrue(SystemMenu.Event.SELECT_LANGUAGE,
                                          select_language))
            .add_transition(ReturningTrue(SystemMenu.Event.SELECT_RECORD,
                                          record_menu))
            .add_transition(ReturningTrue(SystemMenu.Event.DETECT_STORAGE,
                                          initialise_rc1))
            .add_transition(DisconnectingStorage(SystemMenu.Event.DISCONNECT_STORAGE,  # noqa: E501  # pylint: disable=C0301
                                                 system_menu))
            .add_transition(ReturningTrue(SystemMenu.Event.STOP_SYSTEM,
                                          final_state))
            .add_transition(ReturningTrue(SystemMenu.Event.SET_DATE,
                                          set_date))
            .add_transition(ReturningTrue(SystemMenu.Event.SET_TIME,
                                          set_time))
            .add_transition(ReturningTrue(SystemMenu.Event.SET_NAME,
                                          set_name))
        )
        (
            onrecord_menu
            .add_transition(ReturningTrue(OnRecord.Event.MENU,
                                          system_menu))
            .add_transition(SettingCuePoint(OnRecord.Event.SET_CUE,
                                            onrecord_menu))
            .add_transition(TogglingMute(OnRecord.Event.TOGGLE_MUTE,
                                         onrecord_menu))
            .add_transition(StoppingRecording(OnRecord.Event.STOP_RECORDING,
                                              record_menu))
            .add_transition(ShowingStatus(OnRecord.Event.SHOW_STATUS,
                                          onrecord_menu))
            .add_transition(StoppingSystem(OnRecord.Event.STOP_SYSTEM,
                                           final_state))
        )
        (
            record_menu
            .add_transition(ReturningTrue(Record.Event.MENU,
                                          system_menu))
            .add_transition(StartingRecording(Record.Event.START_RECORDING,
                                              onrecord_menu))
            .add_transition(MountingStorage(Record.Event.MOUNT_STORAGE,
                                            final_state))
            .add_transition(DisconnectingStorage(Record.Event.DISCONNECT_STORAGE,  # noqa: E501  # pylint: disable=C0301
                                                 system_menu))
            .add_transition(StoppingSystem(Record.Event.STOP_SYSTEM,
                                           final_state))
            .add_transition(SettingDate(Record.Event.SET_DATE,
                                        set_date))
        )
        (
            initialise_audio
            .add_transition(InitialisingAudio(InitialiseAudio.Event.INIT_AUDIO,
                                              record_menu))
            .add_transition(InitialisingAudio(InitialiseAudio.Event.SKIP_AUDIO,
                                              system_menu))
        )
        (
            set_name
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_0, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_1, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_2, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_3, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_4, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_5, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_6, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_7, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_8, set_name))
            .add_transition(ProcessingDigit(SetName.Event.DIGIT_9, set_name))
            .add_transition(ProcessingDigit(SetName.Event.BACK_SPACE, set_name))  # noqa: E501  ## pylint: disable=C0301
            .add_transition(ProcessingDigit(SetName.Event.ENTER, set_name))
            .add_transition(ReturningTrue(SetName.Event.JUMP_NEXT, initialise_audio))  # noqa: E501  ## pylint: disable=C0301
        )
        (
            set_time
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_0, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_1, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_2, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_3, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_4, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_5, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_6, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_7, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_8, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.DIGIT_9, set_time))
            .add_transition(ProcessingDigit(SetTime.Event.BACK_SPACE, set_time))  # noqa: E501  ## pylint: disable=C0301
            .add_transition(ProcessingDigit(SetTime.Event.ENTER, set_time))
            .add_transition(ReturningTrue(SetTime.Event.JUMP_NEXT, set_name))
        )
        (
            set_date
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_0, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_1, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_2, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_3, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_4, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_5, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_6, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_7, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_8, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.DIGIT_9, set_date))
            .add_transition(ProcessingDigit(SetDate.Event.BACK_SPACE, set_date))  # noqa: E501  ## pylint: disable=C0301
            .add_transition(ProcessingDigit(SetDate.Event.ENTER, set_date))
            .add_transition(ReturningTrue(SetDate.Event.JUMP_NEXT, set_time))
        )
        (
            initialise_rc2
            .add_transition(ReturningTrue(InitialiseRc2.Event.MENU,
                                          system_menu))
            .add_transition(DetectingRc2(InitialiseRc2.Event.DETECT_DEVICE,
                                         set_date))
            .add_transition(SkippingRc2(InitialiseRc2.Event.SKIP_DEVICE,
                                        set_date))
            .add_transition(CleaningRc2(InitialiseRc2.Event.CLEAN_DEVICE,
                                        initialise_rc2))
            .add_transition(MountingRc2(InitialiseRc2.Event.MOUNT_DEVICE,
                                        initialise_rc2))
            .add_transition(UnmountingRc2(InitialiseRc2.Event.UNMOUNT_DEVICE,
                                          initialise_rc2))
        )
        (
            initialise_rc1
            .add_transition(ReturningTrue(InitialiseRc1.Event.MENU,
                                          system_menu))
            .add_transition(DetectingRc1(InitialiseRc1.Event.DETECT_DEVICE,
                                         initialise_rc2))
            .add_transition(SkippingRc1(InitialiseRc1.Event.SKIP_DEVICE,
                                        initialise_rc2))
            .add_transition(CleaningRc1(InitialiseRc1.Event.CLEAN_DEVICE,
                                        initialise_rc1))
            .add_transition(MountingRc1(InitialiseRc1.Event.MOUNT_DEVICE,
                                        initialise_rc1))
            .add_transition(UnmountingRc1(InitialiseRc1.Event.UNMOUNT_DEVICE,
                                          initialise_rc1))
        )
        (
            initialise_ex2
            .add_transition(DetectingEx2(InitialiseEx2.Event.DETECT_DEVICE,
                                         initialise_rc1))
            .add_transition(SkippingEx2(InitialiseEx2.Event.SKIP_DEVICE,
                                        initialise_rc1))
        )
        (
            initialise_ex1
            .add_transition(DetectingEx1(InitialiseEx1.Event.DETECT_DEVICE,
                                         initialise_ex2))
            .add_transition(SkippingEx1(InitialiseEx1.Event.SKIP_DEVICE,
                                        initialise_ex2))
        )
        (
            select_language
            .add_transition(ReturningTrue(
                SelectLanguage.Event.MENU,
                system_menu))
            .add_transition(SelectingEnglish(
                SelectLanguage.Event.SELECT_ENGLISH,
                initialise_ex1))
            .add_transition(SelectingGerman(
                SelectLanguage.Event.SELECT_GERMAN,
                initialise_ex1))
            .add_transition(SelectingFrench(
                SelectLanguage.Event.SELECT_FRENCH,
                initialise_ex1))
            .add_transition(SelectingItalian(
                SelectLanguage.Event.SELECT_ITALIAN,
                initialise_ex1))
        )
        (
            initialise_hi1
            .add_transition(DetectingHi1(InitialiseHi1.Event.DETECT_DEVICE,
                                         select_language))
            .add_transition(SkippingHi1(InitialiseHi1.Event.SKIP_DEVICE,
                                        select_language))
        )
        (
            initialise_lcl
            .add_transition(ReturningTrue(InitialiseLcl.Event.MENU,
                                          system_menu))
            .add_transition(DetectingLcl(InitialiseLcl.Event.DETECT_DEVICE,
                                         initialise_hi1))
            .add_transition(SkippingLcl(InitialiseLcl.Event.SKIP_DEVICE,
                                        initialise_hi1))
        )

        self._ctx = ExecutionContext(None, None, events=self._queue)
        # DFTODO - adjust to something dynamic.
        ui = UserInteractionAudio("system")
        self._fsm = Fsm(initialise_lcl, self._ctx, ui)
        self._fsm.start()

        # for line in self._fsm.visualise():
        #     log.debug(line)

        log.info("Initialising state machine OK.")

    def invoke(self, event: str) -> None:
        """Invoke an event on the state machine."""

        assert event and isinstance(event, str) and 1 == len(event)

        self._queue.enqueue(event)
