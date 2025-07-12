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

"""Module selecting_language_base."""

from biz.dfch.logging import log
from biz.dfch.i18n import LanguageCode
from ...app import ApplicationContext
from ..fsm import StateBase
from ..fsm import TransitionBase
from ..fsm import UiEventInfo


# pylint: disable=R0903
class SelectingLanguageBase(TransitionBase):
    """Base class for selecing language"""

    _language: LanguageCode
    _app_ctx: ApplicationContext

    # pylint: disable=R0913
    # pylint: disable=R0917
    def __init__(
            self,
            event: str,
            info_enter: UiEventInfo,
            info_leave: UiEventInfo,
            target_state: StateBase,
            language: LanguageCode
    ) -> None:

        super().__init__(
            event=event,
            info_enter=info_enter,
            info_leave=info_leave,
            target_state=target_state
        )

        assert language and isinstance(language, LanguageCode)

        self._language = language
        self._app_ctx = ApplicationContext.Factory.get()

    def invoke(self, _) -> bool:

        previous = self._app_ctx.ui_parameters.language
        self._app_ctx.ui_parameters.language = self._language

        log.info("Set language from '%s' to '%s'.",
                 previous,
                 self._app_ctx.ui_parameters.language)

        return True
