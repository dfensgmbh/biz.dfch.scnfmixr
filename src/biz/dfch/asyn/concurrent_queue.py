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

"""Module concurrent_queue."""

import queue
import threading
from typing import overload, TypeVar

T = TypeVar("T")


class ConcurrentQueue:
    """Implements a thread safe FIFO queue.

    Note: though `queue.Queue` itself is thread safe, operations like
    `empty()`are not. Therefore all queue operations are locked."""

    def __init__(self, do_raise: bool = False):
        """Creates an instance of this class.

        Args:
            do_raise (bool): If true, queue.Empty and TimeoutError exceptions
                are raised; if false, only None is returned.
        """

        self._queue = queue.Queue()
        self._sync_root = threading.Lock()
        self._do_raise = do_raise

    @property
    def is_empty(self) -> bool:
        """Determines whether the queue is empty or not.

        Returns:
            bool: True if the queue is empty; false otherwise.
        """

        with self._sync_root:
            return self._queue.empty()

    @property
    def size(self) -> int:
        """Returns the size of items in the quwue."""

        with self._sync_root:
            return self._queue.qsize()

    def enqueue(self, item: object) -> None:
        """Enqueues an item into the queue.

        Blocks until the item could be enqueued.

        Args:
            item (object): The object to be inserted.

        Raises:
            AssertionError: If item is None.
        """

        assert item is not None

        with self._sync_root:
            self._queue.put(item)

    @overload
    def dequeue(self) -> object | None:
        """Dequeues an item from the queue.

        This operation does not wait and returns immediately

        Args:
            None:

        Returns:
            (object | None): The item or None if the queue was empty.
        """

        ...  # pylint: disable=W2301

    @overload
    def dequeue(self, timeout_ms: int) -> object | None:
        """Dequeues an item from the queue.

        This operation will wait for the specified timeout before returning.

        Args:
            timeout_ms (int): The wait timeout in milliseconds.

        Returns:
            (object | None): The item or None if the queue was empty.
        """

        ...  # pylint: disable=W2301

    def dequeue(self, timeout_ms: int | None = None) -> object | None:
        """Dequeues an item from the queue.

        This operation will wait for the specified timeout before returning.

        Args:
            timeout_ms (int): The non-negative wait timeout in milliseconds. If
                timeout_ms is 0, then the timeout is infitive.

        Returns:
            (object | None): The item or None if the queue was empty.

        Raises:
            AssertionError: If timeout None or < 0.
            queue.Empty: If do_raise=True and queue is empty.
            TimeoutError: If do_raise=True and timeout elapsed.
        """

        assert timeout_ms is None or (
            timeout_ms is not None and 0 <= timeout_ms)

        with self._sync_root:
            result = None

            if self._do_raise:
                if not timeout_ms:
                    result = self._queue.get_nowait()
                else:
                    result = self._queue.get(
                        block=True, timeout=timeout_ms/1000)

                self._queue.task_done()
                return result

            try:
                if not timeout_ms:
                    result = self._queue.get_nowait()
                else:
                    result = self._queue.get(
                        block=True, timeout=timeout_ms/1000)

                self._queue.task_done()

                return result

            except queue.Empty:
                return None

            except TimeoutError:
                return None

    def clear(self) -> None:
        """Clears all items in the queue.

        Args:
            None:

        Returns:
            None:
        """

        with self._sync_root:

            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                    self._queue.task_done()
                except queue.Empty:
                    continue
