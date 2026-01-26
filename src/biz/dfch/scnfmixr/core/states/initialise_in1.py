# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

"""Module initialise_in1."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log
from ...app import ApplicationContext
from ...public import SKIP_USB_PORT
from ...public.audio import AudioDevice
from ...public.input import InputEventMap
from ...public.system.messages import SystemMessage
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class InitialiseIn1(StateBase):
    """External insert/effect IN1 detection.

    Detects the external input/output (insert IN1).
    """

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        DETECT_DEVICE = InputEventMap.KEY_1
        SKIP_DEVICE = InputEventMap.KEY_2

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.INITIALISE_IN1_ENTER, True),
            info_leave=None,
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        if ctx.error:
            return

        app_ctx = ApplicationContext.Factory.get()
        value = app_ctx.audio_device_map[AudioDevice.IN1]
        if SKIP_USB_PORT == value:
            log.info("Skipping device '%s' ...", AudioDevice.IN1.name)
            msg = SystemMessage.InputEvent(InitialiseIn1.Event.SKIP_DEVICE)
            ctx.events.publish_first(msg)
            return

        log.info("Enqueueing event: '%s' [%s].",
                 InitialiseIn1.Event.DETECT_DEVICE.name,
                 InitialiseIn1.Event.DETECT_DEVICE.value)

        msg = SystemMessage.InputEvent(InitialiseIn1.Event.DETECT_DEVICE)
        ctx.events.publish_first(msg)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
