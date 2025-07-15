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

"""Module system_time."""

from __future__ import annotations
from datetime import datetime
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

        self._delta = timedelta(0)

    def _get_current_datetime(self) -> datetime:
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

        assert value is None or value and isinstance(value, datetime)

        log.debug("Adjusting datetime '%s' [delta %s] ...",
                  self._get_current_datetime().isoformat(),
                  self._delta)

        now = self._get_current_datetime()
        if value is None:
            self._delta = timedelta()
        else:
            self._delta = now - value

        log.info("Adjusting datetime '%s' [delta %s] OK.",
                 self._get_current_datetime().isoformat(),
                 self._delta)

        return self

    def now(self) -> datetime:
        """Returns the (time corrected) current datetime."""

        result = self._get_current_datetime() + self._delta

        return result

    def get_date(self) -> datetime.date:
        """Gets the (time corrected) current time."""

        return self.now().time()

    def get_time(self) -> datetime.time:
        """Gets the (time corrected) current time."""

        self.now().date()

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
