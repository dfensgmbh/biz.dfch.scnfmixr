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

"""Module playback."""

from __future__ import annotations
from enum import StrEnum

from ...public.input import InputEventMap
from ...public.messages.audio_playback import AudioPlayback
from ...playback.audio_playback import AudioPlayback as player
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..transitions import SelectingResume


__all__ = [
    "Playback",
    "PlaybackPaused",
]


class PlaybackPaused(StateBase):
    """Implements the playback menu when it is paused."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        PAUSE_RESUME = InputEventMap.KEY_0
        MENU = InputEventMap.KEY_5

    def __init__(self):
        super().__init__(
            info_enter=None,
            info_leave=None,
        )


class Playback(StateBase):
    """Implements the playback menu."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        PAUSE_RESUME = InputEventMap.KEY_0
        JUMP_CLIP_END = InputEventMap.KEY_1
        SEEK_NEXT = InputEventMap.KEY_2
        JUMP_CUE_NEXT = InputEventMap.KEY_3
        JUMP_CLIP_PREVIOUS = InputEventMap.KEY_4
        MENU = InputEventMap.KEY_5
        JUMP_CLIP_NEXT = InputEventMap.KEY_6
        JUMP_CLIP_START = InputEventMap.KEY_7
        SEEK_PREVIOUS = InputEventMap.KEY_8
        JUMP_CUE_PREVIOUS = InputEventMap.KEY_9

    def __init__(self):
        super().__init__(
            info_enter=None,
            info_leave=None,
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        # Do not initialize upon entering from self.
        if self == ctx.previous:
            return
        # Do not initialize upon transitioning from SelectingPause.
        if SelectingResume.__name__ == ctx.source:
            return

        # get / acquire are idempotent - safe to call them multiple times.
        player.Factory.get()

        # The start message shall be sent nevertheless.
        ctx.events.publish(AudioPlayback.PlaybackStartCommand())

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
