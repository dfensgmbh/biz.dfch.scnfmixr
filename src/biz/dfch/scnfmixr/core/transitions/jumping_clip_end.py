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

"""Module jumping_clip_end."""

from ...public.messages.audio_playback import AudioPlayback
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext

__all__ = [
    "JumpingClipEnd",
]


class JumpingClipEnd(TransitionBase):  # pylint: disable=R0903
    """Go to end of clip."""

    def __init__(self, event: str, target: StateBase):

        assert isinstance(event, str) and event.strip()
        assert isinstance(target, StateBase)

        super().__init__(
            event,
            info_enter=None,
            info_leave=None,
            target_state=target)

    def invoke(self, ctx: ExecutionContext):

        assert isinstance(ctx, ExecutionContext)

        ctx.events.publish(AudioPlayback.ClipEndCommand())

        return True
