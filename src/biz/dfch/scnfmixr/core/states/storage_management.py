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

"""Module storage_management."""

from enum import StrEnum

from biz.dfch.scnfmixr.core.fsm import ExecutionContext, StateBase, UiEventInfo
from biz.dfch.scnfmixr.core.state_event import StateEvent
from biz.dfch.scnfmixr.public.input import InputEventMap


class StorageManagement(StateBase):
    """Implements StorageManagement menu of the application."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        MENU = InputEventMap.KEY_5
        DISCONNECT_STORAGE = InputEventMap.KEY_0
        DETECT_RC1 = InputEventMap.KEY_1
        DETECT_RC2 = InputEventMap.KEY_3
        FORMAT_RC1 = InputEventMap.KEY_4
        FORMAT_RC2 = InputEventMap.KEY_6
        CLEAN_RC1 = InputEventMap.KEY_7
        CLEAN_RC2 = InputEventMap.KEY_9

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(StateEvent.STORAGE_MANAGEMENT_ENTER, True),
            info_leave=None,
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
