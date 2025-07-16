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

"""Module message_queue."""

from collections import deque
from threading import Lock
from typing import Generic, TypeVar, Optional


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
        """Enqeueus an item at the end of the queue."""

        assert item is not None

        with self._sync_root:
            self._queue.append(item)

    def enqueue_first(self, item: T) -> None:
        """Inserts an item at the top of the queue."""

        assert item is not None

        with self._sync_root:
            self._queue.appendleft(item)

    def dequeue(self) -> Optional[T]:
        """Dequeues an item from the top of the queue."""

        with self._sync_root:
            if not self._queue:
                return None
            return self._queue.popleft()

    def peek(self) -> Optional[T]:
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
