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
