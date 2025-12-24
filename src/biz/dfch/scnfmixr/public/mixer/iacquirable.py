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

"""Module iacquirable."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self


class IAcquirable(ABC):
    """Lifecycle management interface."""

    @property
    @abstractmethod
    def is_acquired(self) -> bool:
        """Determines whether the underlying resource is currently acquired, or
        not."""

    @is_acquired.setter
    @abstractmethod
    def is_acquired(self, value) -> bool:
        """Sets the state whether the underlying resource is currently
        acquired, or not."""

    def __enter__(self) -> Self:
        """ResourceManager: Acquires a resource."""
        return self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        """ResourceManager: Releases a resource."""
        self.release()

    @abstractmethod
    def acquire(self) -> Self:
        """Acquires a resource."""

    @abstractmethod
    def release(self) -> None:
        """Releases a resource."""
