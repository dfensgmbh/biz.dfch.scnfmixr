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

"""Module set_date."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log

from ...app import ApplicationContext
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class SetDate(StateBase):
    """Implements Date input processing."""

    class Events(StrEnum):
        """Events for this state."""

        DIGIT_0 = "0"
        DIGIT_1 = "1"
        DIGIT_2 = "2"
        DIGIT_3 = "3"
        DIGIT_4 = "4"
        DIGIT_5 = "5"
        DIGIT_6 = "6"
        DIGIT_7 = "7"
        DIGIT_8 = "8"
        DIGIT_9 = "9"
        BACK_SPACE = "£"
        ENTER = "!"
        JUMP_NEXT = "|"

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.SET_DATE_ENTER, True),
            info_leave=UiEventInfo(
                StateEvent.SET_DATE_LEAVE, False)
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
                     SetDate.Events.JUMP_NEXT.name,
                     SetDate.Events.JUMP_NEXT.value)
            ctx.events.clear()
            ctx.events.enqueue(SetDate.Events.JUMP_NEXT)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
