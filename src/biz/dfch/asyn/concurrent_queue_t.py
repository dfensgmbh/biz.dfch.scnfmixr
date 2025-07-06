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

"""Module concurrent_queue_t."""

from typing import Generic, overload, TypeVar

from .concurrent_queue import ConcurrentQueue

__all__ = [
    "ConcurrentQueueT",
    "T",
]

T = TypeVar('T')


class ConcurrentQueueT(ConcurrentQueue, Generic[T]):
    """Implements a generic thread safe FIFO queue."""

    def __init__(self, _type: type[T], do_raise: bool = False):

        super().__init__(do_raise)

        assert _type is not None
        self._type = _type

    def enqueue(self, item: T) -> None:

        assert item is not None and isinstance(
            item, self._type), f"{self._type} != {type(item)}"

        super().enqueue(item)

    @overload
    def dequeue(self) -> T | None:
        ...

    @overload
    def dequeue(self, timeout_ms: int) -> T | None:  # pylint: disable=W0221
        ...

    def dequeue(self, timeout_ms: int | None = None) -> T | None:

        result = super().dequeue(timeout_ms)

        assert result is None or isinstance(result, self._type)

        return result
