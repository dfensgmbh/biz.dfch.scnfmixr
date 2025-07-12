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

"""Module implementing LanguageSelection of the application."""

from __future__ import annotations
from enum import StrEnum

from biz.dfch.logging import log
from biz.dfch.i18n import LanguageCode

from ...app import ApplicationContext
from ...ui import UiEventInfo
from ...ui import ExecutionContext
from ...ui import StateBase
from ..state_event import StateEvent


class SelectLanguage(StateBase):
    """Implements LanguageSelection of the application."""

    class Events(StrEnum):
        """Events for this state."""

        MENU = "0"
        SELECT_ENGLISH = "1"
        SELECT_GERMAN = "2"
        SELECT_FRENCH = "3"
        SELECT_ITALIAN = "4"
        EXIT = "5"

    def __init__(self):
        """Default ctor."""

        super().__init__(
            info_enter=UiEventInfo(
                StateEvent.SELECT_LANGUAGE_ENTER, True),
            info_leave=UiEventInfo(
                StateEvent.SELECT_LANGUAGE_LEAVE, False)
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
                ctx.events.enqueue(SelectLanguage.Events.SELECT_ENGLISH)
            case LanguageCode.DE:
                ctx.events.enqueue(SelectLanguage.Events.SELECT_GERMAN)
            case LanguageCode.FR:
                ctx.events.enqueue(SelectLanguage.Events.SELECT_FRENCH)
            case LanguageCode.IT:
                ctx.events.enqueue(SelectLanguage.Events.SELECT_ITALIAN)
            case _:
                pass

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx and isinstance(ctx, ExecutionContext)
