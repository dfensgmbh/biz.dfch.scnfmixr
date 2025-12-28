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

"""Module main."""

from __future__ import annotations
from enum import StrEnum

from ...public.input import InputEventMap
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class Main(StateBase):
    """Implements the main menu."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        START_RECORDING_MX0 = InputEventMap.KEY_1
        START_RECORDING_MX1 = InputEventMap.KEY_2
        START_RECORDING_MX2 = InputEventMap.KEY_3
        START_PLAYBACK = InputEventMap.KEY_4
        MENU = InputEventMap.KEY_5
        SET_NAME = InputEventMap.KEY_6
        DELETE_LAST_TAKE = InputEventMap.KEY_7
        STOP_SYSTEM = InputEventMap.KEY_9

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(StateEvent.MAIN_ENTER, True),
            info_leave=UiEventInfo(
                StateEvent.SWALLOW_STATE_ENTER_LEAVE, False),
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
