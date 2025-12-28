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

"""Module system_menu."""

from __future__ import annotations
from enum import StrEnum

from ...public.input import InputEventMap
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class System(StateBase):
    """Implements the System menu of the application."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        SELECT_MAIN = InputEventMap.KEY_1
        SELECT_LANGUAGE = InputEventMap.KEY_2
        SELECT_STORAGE = InputEventMap.KEY_3
        SET_DATE = InputEventMap.KEY_4
        SET_TIME = InputEventMap.KEY_6
        STOP_SYSTEM = InputEventMap.KEY_9

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(StateEvent.SYSTEM_ENTER, True),
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
