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

from ...system import MessageQueue
from ...public.messages.audio_playback import AudioPlayback

from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class Playback(StateBase):
    """Implements the playback menu."""

    class Event(StrEnum):
        """Events for this state."""

        PAUSE_RESUME = "0"
        JUMP_CLIP_END = "1"
        JUMP_CUE_PREVIOUS = "2"
        JUMP_CLIP_PREVIOUS = "3"
        SEEK_PREVIOUS = "4"
        MENU = "5"
        SEEK_NEXT = "6"
        JUMP_CLIP_START = "7"
        JUMP_CUE_NEXT = "8"
        JUMP_CLIP_NEXT = "9"

    def __init__(self):
        super().__init__(
            info_enter=UiEventInfo(StateEvent.PLAYBACK_ENTER, True),
            info_leave=UiEventInfo(StateEvent.PLAYBACK_LEAVE, True),
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        if type(self).__name__ != ctx.previous:
            return

        MessageQueue.Factory.get().publish(AudioPlayback.PlaybackStartCommand())

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
