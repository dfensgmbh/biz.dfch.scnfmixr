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
import os
from datetime import datetime


__all__ = [
    "FileName"
]


class FileName:  # pylint: disable=R0903
    """Represents a file name."""

    _EXTENSION_DOT = '.'
    _value: str

    def __init__(
            self,
            path_name: str,
            base_name: str,
            dt: datetime,
            suffix: str,
            separator: str = "--",
            extension: str = "flac"
    ) -> None:
        """Creates an instance of the object."""

        assert path_name and path_name.strip()
        assert base_name and base_name.strip()
        assert suffix and suffix.strip()
        assert dt and isinstance(dt, datetime)

        file_name = (
            f"{base_name}"
            f"{separator}"
            f"{dt.strftime('%Y-%m-%d---%H-%M-%S')}"
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

    def delete(self) -> bool:
        """Removes an existing file.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: Any other execption raised by `os.remove`.
        """

        if not self.exists:
            raise FileNotFoundError(self._value)

        os.remove(self._value)

    def __str__(self):
        return self._value

    def __repl__(self):
        return self.__str__
