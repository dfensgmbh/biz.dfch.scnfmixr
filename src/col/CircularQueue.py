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

from collections import deque
from threading import Lock
from typing import Callable, Deque, Generic, Sequence, TypeVar

__all__ = [
    "CircularQueue",
]


T = TypeVar("T")


class CircularQueue(Generic[T]):
    """A circular thread-safe, non-blocking queue that supports a size limit."""

    def __init__(self, max_size: int = -1):
        """Initialises an instance of `CircularQueue` and optionally limits its
        maximum size.

        Args:
            max_size (int): The size of items of the queue, or no size limit if
                set to `-1` (*default*).

        Returns:
            None:
        """

        assert -1 <= max_size

        self._lock = Lock()
        self._queue: Deque[T] = deque(
            maxlen=None if max_size == -1 else max_size)

    def __len__(self) -> int:
        """Returns the number of items in the queue.
        Args:
        Returns:
            int: The number of items in the queue.
        """

        with self._lock:
            return len(self._queue)

    @property
    def has_items(self) -> bool:
        """Returns `True` if the queue contains items. Returns `False`
        otherwise.

        Args:
            None:

        Returns:
            bool: true if the queue contains items; false otherwise.
        """

        with self._lock:
            return bool(self._queue)

    def enqueue(self, item: T) -> int:
        """Enqueue `item` as the newest element on the queue. If current queue
        length equals max_size` the oldest item is overwritten by this
        operation.

        Args:
            item (T): The `item` to enqueue. Must not be `None`.

        Returns:
            int: The length of the queue after enqueuing `item`.
        """

        assert item is not None

        with self._lock:
            self._queue.append(item)

            return len(self._queue)

    def dequeue(self) -> T | None:
        """Returns the oldest items from the queue, or `None` if queue is empty.
        Returns:
            T: The dequeued item, if queue is not empty. Otherwise `None`.
        """

        with self._lock:
            if not self._queue:
                return None

            return self._queue.popleft()

    def dequeue_filter(self, predicate: Callable[[T], bool]) -> Sequence[T]:

        result = []
        with self._lock:
            for i in range(len(self._queue) - 1, -1, -1):

                candidate = self._queue[i]
                if not predicate(candidate):
                    continue

                result.append(candidate)
                del self._queue[i]

        result.reverse()
        return result
