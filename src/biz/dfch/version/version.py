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

"""Module version."""

import sys


class Version:
    """Version class ensuring minimum Python interpreter version."""

    def ensure_minimum_version(self, major: int = 3, minor: int = 11) -> None:
        """Ensures the currently running Python interpreter runs at least the
        specified version.

        Args:
            major (int): The minimum major version required.
            minor (int): The minimum minor version required.

        Returns:
            None:

        Raises:
            EnvironmentError: The exception is raised, when the specified
                version is not met by the currently running Python interpreter.
        """

        if sys.version_info >= (major, minor):
            return

        raise EnvironmentError(f"'{sys.version_info}' < '{major}.{minor}'")
