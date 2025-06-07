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

from collections import deque
from threading import Lock
from typing import Any

from log import log

__all__ = [
    "CircularQueue",
]


class CircularQueue:
    """A circular thread-safe, non-blocking queue that supports a size limit."""

    def __init__(self, max_size: int = -1):
        """Initialises an instance of `CircularQueue` and optionally limits its maximum size.
        Args:
            max_size (int): The size of items of the queue, or no size limit if set to `-1` (*default*).
        Returns:
        """

        assert -1 <= max_size

        self._lock = Lock()
        self._queue = deque(maxlen=None if max_size == -1 else max_size)

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
        """Returns `True` if the queue contains items. Returns `False` otherwise..
        Args:
        Returns:
            bool: `True` if the queue contains items. `False` otherwise.
        """

        with self._lock:
            return bool(self._queue)

    def enqueue(self, item: Any) -> int:
        """Enqueue `item` as the newest element on the queue. If current queue length equals
            `max_size` the oldest item is overwritten by this operation.
        Args:
            item (Any): The `item` to enqueue. Must not be `None`.
        Returns:
            int: The length of the queue after enqueuing `item`.
        """

        assert item is not None

        with self._lock:
            self._queue.append(item)

            return len(self._queue)

    def dequeue(self) -> Any:
        """Returns the oldest items from the queue, or `None` if queue is empty."""

        with self._lock:
            if not self._queue:
                return None

            return self._queue.popleft()
