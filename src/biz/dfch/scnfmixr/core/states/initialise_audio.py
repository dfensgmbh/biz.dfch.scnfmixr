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

"""Module initialise_audio."""

from __future__ import annotations
from enum import StrEnum
import time

from biz.dfch.logging import log
from ...public.input import InputEventMap
from ...public.system.messages import SystemMessage
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class InitialiseAudio(StateBase):
    """Initialise audio system."""

    _WAIT_TIMEOUT_MS = 5000

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        INIT_AUDIO = InputEventMap.KEY_1
        # DFTODO: why would we ever skip audio initialisation?
        SKIP_AUDIO = InputEventMap.KEY_2

    def __init__(self):

        super().__init__(
            info_enter=None,
            info_leave=UiEventInfo(
                StateEvent.INIT_AUDIO_LEAVE, False)
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        # If state machine was just started, we loop until transition succeeds.
        if not ctx.error:

            # If detection failed, we wait before the next attempt.
            # DFTODO - ugly to hard code the class name; but importing it
            # fails, due to a circular reference.
            if ctx.error == "InitializingAudio":
                time.sleep(self._WAIT_TIMEOUT_MS / 1000)

            log.info("Enqueueing event: '%s' [%s].",
                     InitialiseAudio.Event.INIT_AUDIO.name,
                     InitialiseAudio.Event.INIT_AUDIO.value)

            msg = SystemMessage.InputEvent(InitialiseAudio.Event.INIT_AUDIO)
            ctx.events.publish_first(msg)

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
