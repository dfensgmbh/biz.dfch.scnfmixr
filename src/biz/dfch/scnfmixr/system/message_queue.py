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

from __future__ import annotations
from collections.abc import Iterable
from time import sleep
from typing import Generic, TypeVar, Optional, ClassVar, Callable
from threading import Event, Lock, Thread

from biz.dfch.logging import log
from .concurrent_queue_t import ConcurrentQueueT
from ..public.system import MessageBase
# from ..public.system import MessageBase  # pylint: disable=W0611
from ..public.system import MessagePriority


__all__ = [
    "MessageQueueT",
]


T = TypeVar("T", bound="MessageBase")


class MessageQueueT(Generic[T]):  # pylint: disable=R0902
    """Generic message queue."""

    _WORKER_SIGNAL_WAIT_TIME_MS = 1000
    _EXCEPTION_TIMEOUT_MS = 1000

    _queue_high: ConcurrentQueueT[T]
    _queue_default: ConcurrentQueueT[T]
    _callbacks: list[Callable[[MessageBase], None]]
    _is_processing: bool
    _signal: Event
    _worker_do_stop: bool
    _worker_thread: Thread

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not MessageQueueT.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._sync_root = Lock()
        self._queue_high = ConcurrentQueueT[T]()
        self._queue_default = ConcurrentQueueT[T]()
        self._callbacks = []
        self._is_processing = False
        self._signal = Event()
        self._worker_do_stop = False
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

        log.info("Initialising OK.")

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[Optional["MessageQueueT[T]"]] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> "MessageQueueT[T]":
            """Creates or gets the instance of the message queue."""

            if MessageQueueT.Factory.__instance is not None:
                return MessageQueueT.Factory.__instance

            with MessageQueueT.Factory._sync_root:

                if MessageQueueT.Factory.__instance is not None:
                    return MessageQueueT.Factory.__instance

                MessageQueueT.Factory.__instance = MessageQueueT()

            return MessageQueueT.Factory.__instance

    def _process_message(self, message: MessageBase) -> None:
        """Processes a single message."""

        assert message and isinstance(message, MessageBase)

        with self._sync_root:
            callbacks = list(self._callbacks)

        for action in callbacks:
            try:
                log.debug("Dispatching type '%s' [%s] to '%s' ...",
                          message.name,
                          message.priority,
                          action.__qualname__)

                action(message)

                log.info("Dispatching type '%s' [%s] to '%s' OK.",
                         message.name,
                         message.priority,
                         action.__qualname__)

            except Exception as ex:  # pylint: disable=W0718
                log.info("Dispatching type '%s' [%s] to '%s' FAILED. [%s]",
                         message.name,
                         message.priority,
                         action,
                         ex,
                         exc_info=True)

    def _process_messages(self) -> None:
        """Process messages."""

        self._is_processing = True

        try:
            with self._sync_root:

                queue_high = list(self._queue_high)
                self._queue_high.clear()
                queue_default = list(self._queue_default)
                self._queue_default.clear()

            for message in queue_high:
                self._process_message(message)
            for message in queue_default:
                self._process_message(message)

        except Exception as ex:  # pylint: disable=W0718
            log.error("_process_messages: An error occurred: '%s'.",
                      ex,
                      exc_info=True)
        finally:
            self._is_processing = False

    def _worker(self) -> None:
        """Worker thread for processing published message."""

        log.debug("_worker: Initialising ...")

        signal_wait_time_s = self._WORKER_SIGNAL_WAIT_TIME_MS / 1000

        log.info("_worker: Initialising OK.")

        while not self._worker_do_stop:
            try:
                log.debug("_worker: Waiting ...")
                result = self._signal.wait(signal_wait_time_s)
                self._signal.clear()
                if not result:
                    continue

                if self._is_processing:
                    continue

                self._process_messages()

            except Exception as ex:  # pylint: disable=W0718
                log.error("_worker: An error occurred: '%s'. Waiting %sms ...",
                          ex,
                          self._EXCEPTION_TIMEOUT_MS,
                          exc_info=True)
                sleep(self._EXCEPTION_TIMEOUT_MS / 1000)

    def _publish(self, items: T | Iterable[T], at_first: bool) -> None:
        """Internal: Publishes an item to the respective queue.

        Args:
            at_first (bool): True, if the messages should be enqueued at the
                top of the queueu; false, otherwise (defaulT).
        """
        assert items is not None and isinstance(items, (Iterable, MessageBase))

        if not isinstance(items, Iterable):
            items = [items]

        for item in items:
            assert isinstance(item, MessageBase)
            if MessagePriority.HIGH <= item.priority:
                if at_first:
                    self._queue_high.enqueue_first(item)
                else:
                    self._queue_high.enqueue(item)
            else:
                if at_first:
                    self._queue_default.enqueue_first(item)
                else:
                    self._queue_default.enqueue(item)

        self._signal.set()

    def publish(self, items: T | Iterable[T]) -> None:
        """Publishes an item to the respective queue."""

        assert items is not None and isinstance(items, (Iterable, MessageBase))

        self._publish(items, at_first=False)

    def publish_first(self, items: T | Iterable[T]) -> None:
        """Publishes an item to the top of the respective queue."""

        assert items is not None and isinstance(items, (Iterable, MessageBase))

        self._publish(items, at_first=True)

    def clear(self) -> None:
        """Clears all messages from queue."""

        with self._sync_root:
            self._queue_high.clear()
            self._queue_default.clear()

    def _is_registered(
        self, action: Callable[[T], None],
            use_lock: bool
    ) -> bool:
        """Internal: locked and unlocked access to callback."""

        assert action and callable(action)

        if use_lock:
            with self._sync_root:
                result = action in self._callbacks
                return result

        result = any(e for e in self._callbacks if e == action)
        return result

    def is_registered(self, action: Callable[[T], None]) -> bool:
        """Determines, whether a callback is registered or not.

        Returns:
            bool: True, if registered; false, otherwise."""

        assert action and callable(action)

        result = self._is_registered(action, use_lock=True)

        return result

    def register(self, action: Callable[[T], None]) -> bool:
        """Registers a callback on the message queue.

        Calling the method with the same action twice will only register the
        callback once.

        Returns:
            bool: True, if the action was sucessfully registered; false,
                otherwise.
        """

        assert action and callable(action)

        # No double check here, lock directly.
        with self._sync_root:
            if self._is_registered(action, use_lock=False):
                return False

            self._callbacks.append(action)

        return True

    def unregister(self, action: Callable[[T], None]) -> bool:
        """Unregisters a callback on the message queue

        Calling the method with the same action twice will return False.

        Returns:
            bool: True, if the action was sucessfully unregistered; false,
                otherwise.
        """

        assert action and callable(action)

        with self._sync_root:
            try:
                self._callbacks.remove(action)
                return True
            except ValueError:
                return False
