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

"""Module implementing InitialState of the application."""

from __future__ import annotations
from enum import StrEnum
import time

from biz.dfch.logging import log
from ...public.input import InputEventMap
from ...public.system.messages import SystemMessage
from ..fsm import ExecutionContext
from ..fsm import StateBase


class InitialiseLcl(StateBase):
    """Speakerphone LCL Detection.

    Detects the local input/ouput (speakerphone).
    """

    _WAIT_TIMEOUT_MS = 5000

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        DETECT_DEVICE = InputEventMap.KEY_1
        SKIP_DEVICE = InputEventMap.KEY_2

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=None,
            info_leave=None,
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        # If state machine was just started, we loop until transition succeeds.
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
