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

"""Module system_menu."""

from __future__ import annotations
from enum import StrEnum

from ...public.input import InputEventMap
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class System(StateBase):
    """Implements State1 of the application."""

    class Event(StrEnum):
        """Events for this state."""

        # MENU = InputEventMap.KEY_5
        HELP = InputEventMap.KEY_ASTERISK
        SELECT_RECORD = InputEventMap.KEY_1
        SELECT_PLAYBACK = InputEventMap.KEY_2
        SELECT_LANGUAGE = InputEventMap.KEY_3
        SET_DATE = InputEventMap.KEY_4
        SET_TIME = InputEventMap.KEY_5
        SET_NAME = InputEventMap.KEY_6
        DETECT_STORAGE = InputEventMap.KEY_7
        DISCONNECT_STORAGE = InputEventMap.KEY_8
        STOP_SYSTEM = InputEventMap.KEY_9

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(StateEvent.SYSTEM_ENTER, True),
            info_leave=UiEventInfo(StateEvent.SYSTEM_LEAVE, False)
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
