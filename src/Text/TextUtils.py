# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

import os

__all__ = ["TextUtils"]


class TextUtils:
    """Class for reading from text files."""

    def read_first_line(self, file_path: str) -> str:
        """Reads the first text line of the specified file and returns it. File is opened ReadOnly.
        If file_path is not a file, a `FileNotFoundError` is raised.

        Args:
            file_path (str): File to read from in ReadOnly mode.

        Returns:
            str: The first line read from the specified file.
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File does not exist: '{file_path}'.")

        with open(file_path, "r") as file:
            return file.readline().strip()

    def read_all_lines(self, file_path: str) -> list[str]:
        """Reads all lines of the specified file as text and returns it as a list. File is opened ReadOnly.
        If file_path is not a file, a `FileNotFoundError` is thrown.

        Args:
            file_path (str): File to read from in ReadOnly mode.

        Returns:
            list[str]: The contents of file_path as a list of strings.
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File does not exist: '{file_path}'.")

        with open(file_path, "r") as file:
            return file.readlines()
