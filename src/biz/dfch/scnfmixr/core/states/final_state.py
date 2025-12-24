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

"""Module implementing FinalState of the application."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...public.input import InputEventMap
from ...system import MessageQueue
from ..fsm import ExecutionContext
from ..fsm import StateBase

from ...public.system.messages import SystemMessage


class FinalState(StateBase):
    """Implements FinalState of the application."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        MENU = InputEventMap.KEY_5

    def __init__(self):

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

        app_ctx = ApplicationContext.Factory.get()

        mq = MessageQueue.Factory.get()
        mq.publish(SystemMessage.Shutdown())

        log.debug("Initiating application termination ...")

        log.debug("Signalling stop event ...")
        app_ctx.notification.signal_shutdown()
        log.info("Signalling stop event INVOKED.")

        log.debug("Signalling stop state machine ...")
        ctx.signal_stop.set()
        log.info("Signalling stop state machine INVOKED.")

        log.info("Application context: '%s'.", app_ctx)

        log.info("Initiating application termination COMPLETED.")

        return True

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
