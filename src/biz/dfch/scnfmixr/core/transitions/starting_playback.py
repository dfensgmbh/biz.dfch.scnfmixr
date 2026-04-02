# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Module starting_playback."""

from biz.dfch.logging import log

from ...playback.audio_playback import AudioPlayback as AudioPlayer
from ...public.messages import AudioPlayback as msgt
from ...system import FuncExecutor
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent

__all__ = [
    "StartingPlayback",
]


class StartingPlayback(TransitionBase):  # pylint: disable=R0903
    """Start the playback player."""

    def __init__(self, event: str, target: StateBase):

        assert isinstance(event, str) and event.strip()
        assert isinstance(target, StateBase)

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.STARTING_PLAYBACK_LEAVE, False),
            target_state=target)

    def invoke(self, ctx: ExecutionContext) -> bool:

        assert isinstance(ctx, ExecutionContext)

        AudioPlayer.Factory.get()

        with FuncExecutor(
            lambda e: isinstance(e, msgt.StartedNotification),
            lambda e: isinstance(
                e, (msgt.StartedNotification, msgt.PlaybackStopCommand))
        ) as sync:
            result = sync.invoke(
                msgt.PlaybackStartCommand(),
                10)
        result = bool(result)

        if not result:
            log.error("Waiting for playback to start FAILED.")
            return False

        log.info("Waiting for playback to start OK.")
        return True
