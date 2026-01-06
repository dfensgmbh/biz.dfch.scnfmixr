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

"""Module file_name."""

from __future__ import annotations
from datetime import datetime
import os
import re

from ..audio import FileFormat


__all__ = [
    "FileName"
]


class FileName:  # pylint: disable=R0903
    """Represents a file name."""

    _EXTENSION_DOT = '.'
    _FILENAME_PATTERN = (
        r'^(?P<basename>\d{8})\-\-\-'
        r'(?P<date>\d{4}\-\d{2}\-\d{2})\-\-\-'
        r'(?P<time>\d{2}\-\d{2}\-\d{2})\-\-\-'
        r'(?P<suf>[a-zA-Z0-9]{3})\.'
        r'(?P<ext>\w+)$'
    )

    _value: str

    def __init__(
            self,
            path_name: str,
            base_name: str,
            dt: datetime,
            suffix: str,
            dash: str = "-",
            separator: str = "---",
            extension: str = FileFormat.FLAC.value
    ) -> None:
        """Creates an instance of the object."""

        assert path_name and path_name.strip()
        assert base_name and base_name.strip()
        assert suffix and suffix.strip()
        assert dt and isinstance(dt, datetime)

        # format:  basename---yyyy-MM-dd---HH-mm-ss---suf.ext
        # example: 01234567---1927-03-27---08-15-42---MX0.flac
        file_name = (
            f"{base_name}"
            f"{separator}"
            # format:  yyyy-MM-dd---HH-mm-ss
            # example: 1927-03-27---08-15-42
            f"{dt.strftime('%Y')}"
            f"{dash}"
            f"{dt.strftime('%m')}"
            f"{dash}"
            f"{dt.strftime('%d')}"
            f"{separator}"
            f"{dt.strftime('%H')}"
            f"{dash}"
            f"{dt.strftime('%M')}"
            f"{dash}"
            f"{dt.strftime('%S')}"
            f"{separator}"
            f"{suffix}"
            f"{self._EXTENSION_DOT}"
            f"{extension}"
        )

        full_name = os.path.join(path_name, file_name)
        self._value = full_name

    @property
    def exists(self) -> bool:
        """Determines whether the file name exists.

        Returns:
            bool: True, if the file name exists; false, otherwise.
        """

        return os.path.exists(self._value)

    @property
    def direxists(self) -> bool:
        """Determines whether the directory exists.

        Returns:
            bool: True, if the directory exists; false, otherwise.
        """

        return os.path.exists(self.dirname)

    @property
    def dirname(self) -> str:
        """Returns the directory part of the filename."""

        return os.path.dirname(self._value)

    @property
    def filename(self) -> str:
        """Returns the filename part of the filename."""

        return self._value.removeprefix(
            os.path.dirname(self._value)).strip(
                os.path.sep)

    @property
    def fullname(self) -> str:
        """Returns the full name of the file."""

        return self._value

    @staticmethod
    def is_valid_filename(value: str) -> bool:
        """Determines whether a given value matches the file format.

        Args:
            value (str):

        Returns:
            bool: True, if the specified value matches the file format; false,
            otherwise.

        Raises:
            AssertionError: If the specified value is empty or null.
        """

        assert isinstance(value, str) and value.strip()

        match = re.match(FileName._FILENAME_PATTERN, value)
        if not match:
            return False

        parts = match.groupdict()
        ext = parts['ext']
        if ext not in [format.value for format in FileFormat]:
            return False

        return True

    @classmethod
    def from_full_name(cls, value: str) -> FileName:
        """Parses a given filename."""

        assert isinstance(value, str) and value.strip()

        instance = cls.__new__(cls)
        instance._value = value

        return instance

    def delete(self) -> bool:
        """Removes an existing file.

        Returns:
            out[bool]:
                True, if delete is successful. 
                False, if file does not exist or if the file cannot be deleted.
        """

        if not self.exists:
            return False

        try:
            os.remove(self._value)
            return True
        except Exception:  # pylint: disable=W0718
            return False

    def __str__(self):
        return self._value

    def __repl__(self):
        return self.__str__
