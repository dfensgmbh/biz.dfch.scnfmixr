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

"""Module clear_date_time_name."""

from biz.dfch.logging import log

from ...application_context import ApplicationContext

from ..fsm import TransitionBase


# pylint: disable=R0903
class SystemClearDate(TransitionBase):
    """SystemClearDate transition."""

    def invoke(self, _):

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.date_time_name_input.get_date().isoformat()
        log.debug("Clear date '%s'.", value)

        app_ctx.date_time_name_input.clear_date()

        return True


# pylint: disable=R0903
class SystemClearTime(TransitionBase):
    """SystemClearTime transition."""

    def invoke(self, _):

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.date_time_name_input.get_time().isoformat()
        log.debug("Clear time '%s'.", value)

        app_ctx.date_time_name_input.clear_time()

        return True


# pylint: disable=R0903
class SystemClearName(TransitionBase):
    """SystemClearName transition."""

    def invoke(self, _):

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.date_time_name_input.get_name()
        log.debug("Clear name '%s'.", value)

        app_ctx.date_time_name_input.clear_name()

        return True
