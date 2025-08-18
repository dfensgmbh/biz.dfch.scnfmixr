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

"""Module set_time."""

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


class SetTime(StateBase):
    """Implements Time input processing."""

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
                StateEvent.SET_TIME_ENTER, True),
            info_leave=None,
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        app_ctx = ApplicationContext.Factory.get()
        log.info("Time entered: [%s].",
                 app_ctx.date_time_name_input.is_valid_time)

        if not app_ctx.date_time_name_input.is_valid_time:
            return

        log.info("Time fully entered: '%s'.",
                 app_ctx.date_time_name_input.get_time())

        log.info("Enqueueing event: '%s' [%s].",
                 SetTime.Event.JUMP_NEXT.name,
                 SetTime.Event.JUMP_NEXT.value)
        ctx.events.clear()
        msg = SystemMessage.InputEvent(SetTime.Event.JUMP_NEXT)
        ctx.events.publish_first(msg)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
