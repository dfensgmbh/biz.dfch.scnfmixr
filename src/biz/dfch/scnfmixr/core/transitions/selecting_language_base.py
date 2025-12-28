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
