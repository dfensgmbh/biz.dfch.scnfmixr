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

"""Module message_queue."""

from collections import deque
from threading import Lock
from typing import Generic, TypeVar


__all__ = [
    "ConcurrentDoubleSideQueueT",
]


T = TypeVar("T")


class ConcurrentDoubleSideQueueT(Generic[T]):
    """Message queue facility."""

    _sync_root: Lock
    _queue: deque[T]

    def __init__(self):
        """Private ctor."""

        self._sync_root = Lock()
        self._queue = deque()

    def enqueue(self, item: T) -> None:
        """Enqueues an item at the end of the queue."""

        assert item is not None

        with self._sync_root:
            self._queue.append(item)

    def enqueue_first(self, item: T) -> None:
        """Inserts an item at the top of the queue."""

        assert item is not None

        with self._sync_root:
            self._queue.appendleft(item)

    def dequeue(self) -> T | None:
        """Dequeues an item from the top of the queue."""

        with self._sync_root:
            if not self._queue:
                return None
            return self._queue.popleft()

    def peek(self) -> T | None:
        """Returns the top items from dequeue without removing it from the
        queue."""

        with self._sync_root:
            return self._queue[0] if self._queue else None

    def is_empty(self) -> bool:
        """Determines, whether the queue is empty.

        Returns:
            bool: True, if the queue is empty; false, otherwise.
        """

        with self._sync_root:
            return not self._queue

    def clear(self) -> None:
        """Clears the queue."""

        with self._sync_root:
            self._queue.clear()

    def __iter__(self):
        yield from self._queue

    def __len__(self) -> int:
        """Returns the length of the queue."""

        with self._sync_root:
            return len(self._queue)

    def acquire(self) -> None:
        """Manually acquire the queue lock."""

        self._sync_root.acquire()  # pylint: disable=R1732

    def release(self) -> None:
        """Manually release the queue lock."""

        self._sync_root.release()
