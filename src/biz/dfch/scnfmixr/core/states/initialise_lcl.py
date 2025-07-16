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

"""Module implementing InitialState of the application."""

from __future__ import annotations
from enum import StrEnum
import time

from biz.dfch.logging import log
from ...public.system.messages import SystemMessage
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class InitialiseLcl(StateBase):
    """Speakerphone LCL Detection.

    Detects the local input/ouput (speakerphone).
    """

    _WAIT_TIMEOUT_MS = 5000

    class Event(StrEnum):
        """Events for this state."""

        MENU = "0"  # Return to the next menu in the hierarchy.
        DETECT_DEVICE = "1"  # Detect the device.
        SKIP_DEVICE = "2"  # Skip the device.

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.INITIALISE_LCL_ENTER, True),
            info_leave=UiEventInfo(
                StateEvent.INITIALISE_LCL_LEAVE, True)
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        # If state machine was just started, we loop until transistion succeeds.
        if not ctx.previous:

            # If detection failed, we wait before the next attempt.
            # DFTODO - ugly to hard code the class name; but importing it
            # fails, due to a circular reference.
            if ctx.error == "DetectingLcl":
                time.sleep(self._WAIT_TIMEOUT_MS / 1000)

            log.info("Enqueueing event: '%s' [%s].",
                     InitialiseLcl.Event.DETECT_DEVICE.name,
                     InitialiseLcl.Event.DETECT_DEVICE.value)

            msg = SystemMessage.InputEvent(InitialiseLcl.Event.DETECT_DEVICE)
            ctx.events.publish_first(msg)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
