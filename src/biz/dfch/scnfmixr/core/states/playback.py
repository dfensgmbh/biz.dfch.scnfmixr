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

"""Module playback."""

from __future__ import annotations
from enum import StrEnum

from ...public.input import InputEventMap
from ...public.messages.audio_playback import AudioPlayback
from ...playback.audio_playback import AudioPlayback as player
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..transitions import SelectingPause


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

        # Do not initialise upon entering from self.
        if self == ctx.previous:
            return
        # Do not initialise upon transitioning from SelectingPause.
        if SelectingPause.__name__ == ctx.source:
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
