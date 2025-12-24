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

"""Module set_date."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...public.input import InputEventMap
from ...public.system.messages import SystemMessage
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class SetDate(StateBase):
    """Implements Date input processing."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        DIGIT_0 = InputEventMap.KEY_0
        DIGIT_1 = InputEventMap.KEY_1
        DIGIT_2 = InputEventMap.KEY_2
        DIGIT_3 = InputEventMap.KEY_3
        DIGIT_4 = InputEventMap.KEY_4
        DIGIT_5 = InputEventMap.KEY_5
        DIGIT_6 = InputEventMap.KEY_6
        DIGIT_7 = InputEventMap.KEY_7
        DIGIT_8 = InputEventMap.KEY_8
        DIGIT_9 = InputEventMap.KEY_9
        BACK_SPACE = InputEventMap.KEY_BACKSPACE
        ENTER = InputEventMap.KEY_ENTER
        JUMP_NEXT = InputEventMap.KEY_TAB

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.SET_DATE_ENTER, True),
            info_leave=None,
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        app_ctx = ApplicationContext.Factory.get()
        log.info("Date entered: [%s].",
                 app_ctx.date_time_name_input.is_valid_date)

        if app_ctx.date_time_name_input.is_valid_date:

            log.info("Date fully entered: '%s'.",
                     app_ctx.date_time_name_input.get_date())

            log.info("Enqueueing event: '%s' [%s].",
                     SetDate.Event.JUMP_NEXT.name,
                     SetDate.Event.JUMP_NEXT.value)
            ctx.events.clear()
            msg = SystemMessage.InputEvent(SetDate.Event.JUMP_NEXT)
            ctx.events.publish_first(msg)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
