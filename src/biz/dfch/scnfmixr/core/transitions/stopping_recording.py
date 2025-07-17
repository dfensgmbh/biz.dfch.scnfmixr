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

"""Module stopping_recording."""

from threading import Event

from biz.dfch.logging import log

from ...public.system import MessageBase
from ...system import MessageQueue
from ...public.mixer import (
    MixerMessage,
)
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class StoppingRecording(TransitionBase):
    """Stops a recording."""

    _is_recording_stopped: Event

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.STOPPING_RECORDING_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.STOPPING_RECORDING_LEAVE, False),
            target_state=target)

        self._is_recording_stopped = Event()

    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

        if not isinstance(message, MixerMessage.Recorder.StoppedMessage):
            return

        self._is_recording_stopped.set()

    def invoke(self, _):

        self._is_recording_stopped.clear()

        message_queue = MessageQueue.Factory.get()
        message_queue.register(self._on_message)
        message_queue.publish(
            MixerMessage.Recorder.RecordingStopCommand())

        log.debug("Waiting for recording to stop ...")

        result = self._is_recording_stopped.wait(10)
        message_queue.unregister(self._on_message)
        self._is_recording_stopped.clear()

        if result:
            log.info("Waiting for recording to stop OK.")
        else:
            log.error("Waiting for recording to stop FAILED.")

        return result
