# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Module system_time."""

from __future__ import annotations
from datetime import datetime, date, time
from datetime import timedelta
from threading import Lock
from typing import ClassVar

from biz.dfch.logging import log


__all__ = [
    "SystemTime"
]


class SystemTime:  # pylint: disable=R0903
    """Represents the corrected system time."""

    _delta: timedelta

    def __init__(self):

        if not SystemTime.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        self._delta = timedelta()

    def _get_internal_system_current_datetime(self) -> datetime:
        """Internal: gets the current datetime of the underlying system."""

        return datetime.now()

    def set(self, value: datetime | None = None) -> SystemTime:
        """Sets the system date and time.

        Args:
            value (datetime | None): The new datetime to be set. If none,
                datetime will be reset to underlying system time.

        Returns:
            SystemTime: The same instance.
        """

        now = self._get_internal_system_current_datetime()

        assert value is None or value and isinstance(value, datetime)

        log.debug(
            "Adjusting datetime '%s' [delta %s] with value '%s' ...",
            now.isoformat(),
            self._delta,
            value,
        )

        if value is None:
            self._delta = timedelta()
        else:
            self._delta = now - value

        log.info(
            "Adjusting datetime '%s' [delta %s] with value '%s' OK.",
            now.isoformat(),
            self._delta,
            value,
        )

        return self

    def now(self) -> datetime:
        """Returns the (date and time corrected) current datetime."""

        result = self._get_internal_system_current_datetime() - self._delta

        return result

    def get_date(self) -> date:
        """Gets the (date and time corrected) current date."""

        return self.now().date()

    def get_time(self) -> time:
        """Gets the (date and time corrected) current time."""

        return self.now().time()

    class Factory:
        """Factory class for creating `SystemTime` singleton."""

        __instance: ClassVar[SystemTime | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> SystemTime:
            """Creates or gets the `SystemTime` singleton instance.

            Returns:
                SystemTime: An instance of the object.
            """

            if SystemTime.Factory.__instance:
                return SystemTime.Factory.__instance

            with SystemTime.Factory._sync_root:

                if SystemTime.Factory.__instance:
                    return SystemTime.Factory.__instance

                SystemTime.Factory.__instance = SystemTime()

            return SystemTime.Factory.__instance
