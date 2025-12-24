# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""Module providing text file related functions."""

import os

__all__ = ["TextUtils"]


class TextUtils:
    """Class for reading from text files."""

    def read_first_line(self, file_path: str) -> str:
        """Reads the first text line of the specified file and returns it. File is opened ReadOnly. \
        If file_path is not a file, a `FileNotFoundError` is raised.

        Args:
            file_path (str): File to read from in ReadOnly mode.

        Returns:
            str: The first line read from the specified file.

        Raises:
            FileNotFoundException: An an exception is raised, if the specified file is not found.
        """

        assert file_path is not None and "" != file_path.strip()

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File does not exist: '{file_path}'.")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.readline().strip()

    def try_read_first_line(self, file_path: str) -> str | None:
        """Reads the first text line of the specified file and returns it. File is opened ReadOnly.
        If file_path is not a file or cannot be read, `None` is returned.

        Args:
            file_path (str): File to read from in ReadOnly mode.

        Returns:
            str: The first line read from the specified file or `None` if file not found or cannot be read.
        """

        assert file_path is not None and "" != file_path.strip()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readline().strip()
        except Exception:  # pylint: disable=broad-exception-caught
            return None

    def read_all_lines(self, file_path: str) -> list[str]:
        """Reads all lines of the specified file as text and returns it as a list. File is opened ReadOnly.
        If file_path is not a file, a `FileNotFoundError` is thrown.

        Args:
            file_path (str): File to read from in ReadOnly mode.

        Returns:
            list[str]: The contents of file_path as a list of strings.
        """

        assert file_path is not None and "" != file_path.strip()

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File does not exist: '{file_path}'.")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
