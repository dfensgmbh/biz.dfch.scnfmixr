# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
