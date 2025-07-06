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

"""Module implementing FinalState of the application."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...ui import UiEventInfo
from ...ui import ExecutionContext
from ...ui import StateBase
from ..state_event import StateEvent


class FinalState(StateBase):
    """Implements FinalState of the application."""

    class Events(StrEnum):
        """Events for this state."""

        MENU = "0"

    def __init__(self):

        super().__init__(
            info_enter=UiEventInfo(StateEvent.FINAL_STATE_ENTER, False),
            info_leave=UiEventInfo(StateEvent.FINAL_STATE_LEAVE, False)
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        log.info("Stopping state machine.")
        ctx.signal_stop.set()

        app_ctx = ApplicationContext()
        # log.info("Snd map: '%s'.", app_ctx.audio_device_map)
        # log.info("Sto map: '%s'.", app_ctx.storage_device_map)
        # log.info("Inp map: '%s'.", app_ctx.input_device_map)
        # log.info("Rec opt: '%s'.", app_ctx.rec_params)
        log.info("App ctx: '%s'.", app_ctx)

        return True

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
