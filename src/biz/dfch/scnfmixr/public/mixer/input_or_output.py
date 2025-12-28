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

"""Module input_or_output."""

from __future__ import annotations
from abc import ABC, abstractmethod


__all__ = [
    "InputOrOutput",
]


# pylint: disable=R0903
class InputOrOutput(ABC):
    """Represents an input or output object."""

    name: str

    @property
    @abstractmethod
    def is_started(self) -> bool:
        """Determines whether the input or output is started."""

    @abstractmethod
    def invoke(self) -> None:
        """Invokes the object."""

    @abstractmethod
    def start(self) -> bool:
        """Starts the input or output."""

    @abstractmethod
    def stop(self) -> bool:
        """Stops the input or output."""

    @abstractmethod
    def connect_to(
        self,
        other: InputOrOutput,
        idx: int = 0,
        idx_other: int = 0
    ) -> bool:
        """Connects an input object to output object.

        Args:
            other (InputOrOutput): The object to connect to.
            idx (int): The port index of this object to connect from. If `0`,
                all port of this object will be connected (default).
            idx_other (int): The port index of the other object to connect to.
                If `0`, all port of the other object will be connected
                (default).
        """

    def __str__(self) -> str:
        return f"'{self.name}' [{type(self)}]"

    def __repr__(self) -> str:
        return self.__str__()
