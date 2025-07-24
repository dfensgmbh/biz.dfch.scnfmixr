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
