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

"""Module iconnectable_sink_point."""

from __future__ import annotations
from collections.abc import Iterator
from threading import Lock

from .iconnectable_point_or_set import IConnectablePointOrSet
from .iconnectable_point import IConnectablePoint


class IConnectableSet(IConnectablePointOrSet):
    """Represents a connectable signal point set."""

    _sync_root: Lock
    _items: dict[IConnectablePoint, None]

    def __init__(self, name: str):
        super().__init__(name)

        self._sync_root = Lock()
        self._items = {}

    @property
    def is_point(self) -> bool:
        return False

    @property
    def is_set(self) -> bool:
        return True

    @property
    def points(self) -> list[IConnectablePoint]:
        """The associated signal points with this device."""
        return list(self._items.keys())

    def add(self, item: IConnectablePoint) -> None:
        """Adds an item to the set."""

        if not isinstance(item, IConnectablePoint):
            raise ValueError("Invalid item.")

        with self._sync_root:
            if item in self._items:
                raise ValueError("Item already exists.")

            self._items[item] = None

    def remove(self, item: IConnectablePoint):
        """Removes an item from the set."""

        if not isinstance(item, IConnectablePoint):
            raise ValueError("Invalid item.")

        with self._sync_root:
            if item not in self._items:
                raise ValueError("Item not found.")

        del self._items[item]

    def __contains__(self, item: IConnectablePoint) -> bool:
        """Determines whether an item exists in the set, or not."""

        with self._sync_root:
            return item in self._items

    def __iter__(self) -> Iterator[IConnectablePoint]:
        """Returns an iterator of the set."""

        with self._sync_root:
            return iter(self._items.keys())

    def __len__(self) -> int:
        """Returns the number of items in the set."""

        with self._sync_root:
            return len(self._items)

    def clear(self) -> None:
        """Removes all items from the set."""

        with self._sync_root:
            self._items.clear()
