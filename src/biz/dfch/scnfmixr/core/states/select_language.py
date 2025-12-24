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

"""Module implementing LanguageSelection of the application."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log
from biz.dfch.i18n import LanguageCode

from ...public.input import InputEventMap
from ...public.system.messages import SystemMessage
from ...app import ApplicationContext
from ..fsm import UiEventInfo
from ..fsm import ExecutionContext
from ..fsm import StateBase
from ..state_event import StateEvent


class SelectLanguage(StateBase):
    """Implements LanguageSelection of the application."""

    class Event(StrEnum):
        """Events for this state."""

        HELP = InputEventMap.KEY_ASTERISK
        SELECT_ENGLISH = InputEventMap.KEY_1
        SELECT_GERMAN = InputEventMap.KEY_2
        SELECT_FRENCH = InputEventMap.KEY_3
        SELECT_ITALIAN = InputEventMap.KEY_4

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.SELECT_LANGUAGE_ENTER, True),
            info_leave=UiEventInfo(
                StateEvent.SWALLOW_STATE_ENTER_LEAVE, True),
        )

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)

        app_ctx = ApplicationContext.Factory.get()

        # If the language code was not selected via CLI, let the user choose.
        log.debug("Currently selected language: '%s' [%s].",
                  app_ctx.ui_parameters.language.name,
                  app_ctx.ui_parameters.language.value)
        match app_ctx.ui_parameters.language:
            case LanguageCode.EN:
                msg = SystemMessage.InputEvent(
                    SelectLanguage.Event.SELECT_ENGLISH)
                ctx.events.publish_first(msg)
            case LanguageCode.DE:
                msg = SystemMessage.InputEvent(
                    SelectLanguage.Event.SELECT_GERMAN)
                ctx.events.publish_first(msg)
            case LanguageCode.FR:
                msg = SystemMessage.InputEvent(
                    SelectLanguage.Event.SELECT_FRENCH)
                ctx.events.publish_first(msg)
            case LanguageCode.IT:
                msg = SystemMessage.InputEvent(
                    SelectLanguage.Event.SELECT_ITALIAN)
                ctx.events.publish_first(msg)
            case _:
                pass

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
