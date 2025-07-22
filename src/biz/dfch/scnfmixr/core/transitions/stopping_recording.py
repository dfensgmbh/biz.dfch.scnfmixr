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

from biz.dfch.logging import log

from ...public.messages import AudioRecorder as msgt
from ...system import FuncExecutor
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class StoppingRecording(TransitionBase):
    """Stops a recording."""

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.STOPPING_RECORDING_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.STOPPING_RECORDING_LEAVE, False),
            target_state=target)

    def invoke(self, _):

        log.debug("Waiting for recording to stop ...")

        with FuncExecutor(
            lambda _: True,
            lambda e: isinstance(e, msgt.StoppedNotification)
        ) as sync:
            result = sync.invoke(
                msgt.RecordingStopCommand(),
                10)

        if result:
            log.info("Waiting for recording to stop OK.")
        else:
            log.error("Waiting for recording to stop FAILED.")

        return result
