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

"""Module file_name."""

from __future__ import annotations
from datetime import datetime, timedelta
from os import path
from string import ascii_lowercase
from threading import Lock
from typing import ClassVar, overload

from biz.dfch.logging import log

__all__ = [
    "FileName"
]


# pylint: disable=R0903
class SystemTime:
    """Represents the corrected system time."""

    _delta: timedelta

    def __init__(self, value: timedelta):

        if not SystemTime.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        self._delta = timedelta()

    def _get_current_datetime() -> datetime:
        """Internal: gets the current datetime of the underlying system."""

        return datetime.now()

    def set(self, value: datetime) -> timedelta:
        """Sets the system date and time.
        
        Args:
            value (datetime): The new datetime to be set.
        
        Returns:
            timedelta: The delta between the specified datetime in `value` and
                the datetime of the underlying system.
        """

        assert value and isinstance(value, datetime)

        with SystemTime.Factory._sync_root:

            now = self._get_current_datetime()

            self._delta = now - value

        return self._delta

    @property
    def now(self) -> datetime:
        """Returns the current datetime."""

        result = self._get_current_datetime + self._delta

        return result

    class Factory:
        """Factory class for creating `SystemTime` singelton."""

        __instance: ClassVar[SystemTime | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> SystemTime:
            """Gets the system time instance."""

            if SystemTime.Factory.__instance:
                return SystemTime.Factory.__instance

            with SystemTime.Factory._sync_root:

                if SystemTime.Factory.__instance:
                    return SystemTime.Factory.__instance

                SystemTime.Factory.__instance = SystemTime()

            return SystemTime.Factory.__instance


class FileName:  # pylint: disable=R0903
    """Represents a file name."""

    _value: str

    def __init__(self, value: str):
        if not FileName.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert value and value.strip()

        self._value = value

    @property
    def exists(self) -> bool:
        """Determines whether the file name exists.

        Returns:
            bool: True, if the file name exists; false, otherwise.
        """

        return path.exists(self._value)

    # pylint: disable=R0903
    class Factory:
        """Factory class for creating `FileName` instances."""

        _SEPARATOR: str = "---"
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def create(
            prefix: str,
            wait_interval_ms: int = 1000,
            suffix: str,
            separator: str = Factory._SEPARATOR
        ) -> FileName:
            """Factory method for creating `FileName` instances.
            """

            assert prefix and prefix.strip()
            assert suffix and suffix.strip()
            assert separator and separator.strip()

            with FileName.Factory._syncroot:
                result = FileName()

            return result
