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

"""Module func_executor."""

from __future__ import annotations
from threading import Event
from typing import Callable, Generic, Self, TypeVar

from ..public.system.message_base import MessageBase
from .message_queue import MessageQueue

__all__ = [
    "FuncExecutor"
]


T = TypeVar("T")


class FuncExecutor(Generic[T]):
    """Publishes a message, waits for a return message and executes a specified
    func returning the result."""

    _exception: Exception | None
    _is_acquired: bool
    _signal: Event
    _result: T | None
    _mq: MessageQueue
    _func: Callable[[MessageBase], T]
    _predicate: Callable[[MessageBase], bool]

    def __init__(
            self,
            func: Callable[[MessageBase], T],
            predicate: Callable[[MessageBase], bool],
    ):

        assert callable(func)
        assert callable(predicate)

        self._exception = None
        self._is_acquired = False
        self._signal = Event()
        self._result = None
        self._mq = MessageQueue.Factory.get()
        self._func = func
        self._predicate = predicate

    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

        assert isinstance(message, MessageBase)

        if self._signal.is_set():
            return

        try:
            self._result = self._func(message)
        except Exception as ex:  # pylint: disable=W0718
            self._exception = ex
        finally:
            self._signal.set()

    def __enter__(self) -> Self:
        return self.acquire()

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.release()

    def acquire(self) -> Self:
        """Register message handler."""

        if self._is_acquired:
            return self

        self._mq.register(self._on_message, self._predicate)
        self._is_acquired = True

        return self

    def release(self) -> None:
        """Unregister message handler."""

        if not self._is_acquired:
            return

        self._mq.unregister(self._on_message)
        self._is_acquired = False

    def get_result(self) -> T | None:
        """Gets the result or raise the exception that occurred inside the
        func."""

        if self._exception is not None:
            raise self._exception

        return self._result

    def invoke(
            self,
            message: MessageBase,
            max_wait_time: float = 5,
    ) -> T | None:
        """Invokes a message and waits for a response."""

        assert 0 < max_wait_time
        assert isinstance(message, MessageBase)

        self._exception = None
        self._result = None
        self._signal.clear()

        self._mq.publish(message)

        self._signal.wait(max_wait_time)

        return self.get_result()

    def wait(
            self,
            max_wait_time: float = 5,
    ) -> T | None:
        """Waits for a message."""

        assert 0 < max_wait_time

        self._exception = None
        self._result = None
        self._signal.clear()

        self._signal.wait(max_wait_time)

        return self.get_result()
