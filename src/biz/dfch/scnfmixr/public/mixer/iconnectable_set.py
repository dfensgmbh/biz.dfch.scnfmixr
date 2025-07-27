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
