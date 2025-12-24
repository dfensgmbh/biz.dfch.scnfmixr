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

"""Module iconnectable_point_or_set."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .connection_policy import ConnectionPolicy
from .iacquirable import IAcquirable

if TYPE_CHECKING:
    from .isignal_path import ISignalPath


class IConnectablePointOrSet(IAcquirable, ABC):
    """Represents a connectable signal point or signal set."""

    name: str

    def __init__(self, name: str):
        super().__init__()

        assert isinstance(name, str) and name.strip()

        self.name = name

    @property
    @abstractmethod
    def is_source(self) -> bool:
        """Determines whether the object is a source or not."""

    @property
    @abstractmethod
    def is_sink(self) -> bool:
        """Determines whether the object is a sink or not."""

    @property
    @abstractmethod
    def is_point(self) -> bool:
        """Determines whether the object is a point or not."""

    @property
    @abstractmethod
    def is_set(self) -> bool:
        """Determines whether the object is a set or not."""

    @abstractmethod
    def connect_to(
        self,
        other: IConnectablePointOrSet,
        policy: ConnectionPolicy = ConnectionPolicy.DEFAULT
    ) -> set["ISignalPath"]:
        """Connect this point set to the other point set.

        Only source and sink can be connected. If both points or sets are source
            or both are sink, the operation will fail.
        """

        assert isinstance(other, IConnectablePointOrSet)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
