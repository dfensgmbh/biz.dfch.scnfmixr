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

"""Module selecting_pause."""

from ...public.messages.audio_playback import AudioPlayback
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent

__all__ = [
    "SelectingPause",
]


class SelectingPause(TransitionBase):  # pylint: disable=R0903
    """Selects playback pause/resume."""

    def __init__(self, event: str, target: StateBase):

        assert isinstance(event, str) and event.strip()
        assert isinstance(target, StateBase)

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.SELECTING_PAUSE_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.SELECTING_PAUSE_LEAVE, False),
            target_state=target)

    def invoke(self, ctx: ExecutionContext):

        assert isinstance(ctx, ExecutionContext)

        ctx.events.publish(AudioPlayback.PauseResumeCommand())

        return True
