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

"""Module iconnectable_point."""

from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from .iconnectable_point_or_set import IConnectablePointOrSet
from .state import State

# DFTODO - can we remove this? currently, the only forward ref is a type hint,
# which can be (and is) quoted.
if TYPE_CHECKING:
    from .isignal_path import ISignalPath


class IConnectablePoint(IConnectablePointOrSet):
    """Represents a connectable signal point."""

    _state: State

    def __init__(self, name: str):
        super().__init__(name)

        assert isinstance(name, str) and name.strip()

        self._state = State()

    @property
    def state(self) -> State:
        """Returns the state of the point."""
        return self._state

    @property
    def is_point(self) -> bool:
        return True

    @property
    def is_set(self) -> bool:
        return False

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """Determines whether the signal point is active."""

    def connect(self, other: IConnectablePoint) -> "ISignalPath":
        """Connects this point to the other."""

        assert isinstance(other, IConnectablePoint)

        # return self.connect_to(other)[0]
        return next(self.connect_to(other), [])
