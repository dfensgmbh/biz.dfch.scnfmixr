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
