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
