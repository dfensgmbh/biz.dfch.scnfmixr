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
from dataclasses import dataclass
from time import sleep
from typing import (
    ClassVar,
    Callable,
)
from threading import Event, Lock, Thread

from biz.dfch.logging import log
from ...asyn import ConcurrentDoubleSideQueueT
from ..public.system import (
    MessageBase,
)
from ..public.system import MessagePriority


__all__ = [
    "MessageQueue",
]


@dataclass(frozen=True)
class ActionDescriptor:
    """A item in the callback list.

    Attributes:
        action: The callback to invoke.
        predicate: The filter to determine, if the callback shall be invoked.
    """

    action: Callable[[MessageBase], None]
    predicate: Callable[[MessageBase], bool] | None = None


class MessageQueue():  # pylint: disable=R0902
    """Generic message queue."""

    _WORKER_SIGNAL_WAIT_TIME_MS = 5000
    _EXCEPTION_TIMEOUT_MS = 1000

    _sync_root: Lock
    _queue_high: ConcurrentDoubleSideQueueT[MessageBase]
    _queue_default: ConcurrentDoubleSideQueueT[MessageBase]
    _callbacks: list[ActionDescriptor]
    _is_processing: bool
    _signal: Event
    _worker_do_stop: bool
    _worker_thread: Thread

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not MessageQueue.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._sync_root = Lock()
        self._queue_high = ConcurrentDoubleSideQueueT[MessageBase]()
        self._queue_default = ConcurrentDoubleSideQueueT[MessageBase]()
        self._callbacks = []
        self._is_processing = False
        self._signal = Event()
        self._worker_do_stop = False
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

        log.info("Initialising OK.")

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[MessageQueue[MessageBase] | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> "MessageQueue[MessageBase]":
            """Creates or gets the instance of the message queue."""

            if MessageQueue.Factory.__instance is not None:
                return MessageQueue.Factory.__instance

            with MessageQueue.Factory._sync_root:

                if MessageQueue.Factory.__instance is not None:
                    return MessageQueue.Factory.__instance

                MessageQueue.Factory.__instance = MessageQueue()

            return MessageQueue.Factory.__instance

    @staticmethod
    def get_fqcn(_type: type) -> str:
        """Returns the full qualified class name."""

        assert _type

        return f"{_type.__module__}.{_type.__qualname__}"

    def _process_message(
            self,
            message: MessageBase,
            callbacks: list[ActionDescriptor]
    ) -> None:
        """Processes a single message."""

        assert message and isinstance(message, MessageBase)

        for item in callbacks:

            try:
                action = item.action
                if callable(item.predicate) and not item.predicate(message):
                    continue

                log.debug("Dispatching type '%s' [%s] to '%s' ...",
                          message.name,
                          message.priority,
                          MessageQueue.get_fqcn(action))

                action(message)

                log.info("Dispatching type '%s' [%s] to '%s' OK.",
                         message.name,
                         message.priority,
                         MessageQueue.get_fqcn(action))

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

        log.debug("Processing messages ... [%s]",
                  len(self._callbacks))

        try:
            with self._sync_root:

                queue_high = list(self._queue_high)
                self._queue_high.clear()
                queue_default = list(self._queue_default)
                self._queue_default.clear()
                callback_item = list(self._callbacks)

            if 0 == len(callback_item):
                log.debug("No actions registered. Discarding messages.")
                return

            for message in queue_high:
                self._process_message(message, callback_item)

            for message in queue_default:
                self._process_message(message, callback_item)

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

    def _publish(
            self,
            items: MessageBase | Iterable[MessageBase],
            at_first: bool
    ) -> None:
        """Internal: Publishes an item to the respective queue.

        Args:
            item (Message | Iterable[MessageBase]): Message to publish.
            at_first (bool): True, if the messages should be enqueued at the
                top of the queueu; false, otherwise (defaulT).
        """
        assert items is not None and isinstance(items, (Iterable, MessageBase))

        if not isinstance(items, Iterable):
            items = [items]

        for item in items:

            assert isinstance(item, MessageBase)

            log.debug("Received '%s' [%s].", item.name, item.priority)

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

    def publish(self, *items: MessageBase | Iterable[MessageBase]) -> None:
        """Publishes an item to the respective queue.

        Args:
            item (Message | Iterable[MessageBase]): Message to publish.
        """

        assert items

        normalised: list[MessageBase] = []

        for item in items:

            assert isinstance(item, (MessageBase, Iterable))

            if isinstance(item, MessageBase):
                normalised.append(item)

            elif isinstance(item, Iterable):
                assert all(isinstance(e, MessageBase) for e in item)
                normalised.extend(item)

        self._publish(normalised, at_first=False)

    def publish_first(self, items: MessageBase | Iterable[MessageBase]) -> None:
        """Publishes an item to the top of the respective queue.

        Args:
            item (Message | Iterable[MessageBase]): Message to publish.
        """

        assert items is not None and isinstance(items, (Iterable, MessageBase))

        self._publish(items, at_first=True)

    def clear(self) -> None:
        """Clears all messages from queue."""

        with self._sync_root:
            self._queue_high.clear()
            self._queue_default.clear()

    def _is_registered(
        self, action: Callable[[MessageBase], None],
            use_lock: bool
    ) -> bool:
        """Internal: locked and unlocked access to callback."""

        assert action and callable(action)

        if use_lock:
            with self._sync_root:
                result = any(e.action is action for e in self._callbacks)
                return result

        result = any(e.action is action for e in self._callbacks)
        return result

    def is_registered(self, action: Callable[[MessageBase], None]) -> bool:
        """Determines, whether a callback is registered or not.

        Returns:
            bool: True, if registered; false, otherwise."""

        assert action and callable(action)

        result = self._is_registered(action, use_lock=True)

        return result

    def register(
            self,
            action: Callable[[MessageBase], None],
            predicate: Callable[[], bool] | None = None
    ) -> bool:
        """Registers a callback on the message queue.

        Calling the method with the same action twice will only register the
        callback once.

        Args:
            action (Callable): The action to invoke.
            predicate (Callable | None): The optional filter to determine if
                an action should be invoked.

        Returns:
            bool: True, if the action was sucessfully registered; false,
                otherwise.
        """

        assert action and callable(action)
        assert predicate is None or predicate and callable(predicate)

        log.debug("Registering action '%s' ... [%s]",
                  MessageQueue.get_fqcn(action),
                  len(self._callbacks))

        # No double check here, lock directly.
        with self._sync_root:
            if self._is_registered(action, use_lock=False):
                log.warning(
                    "Registering action '%s' FAILED. Already registered. [%s]",
                    MessageQueue.get_fqcn(action),
                    len(self._callbacks))
                return False

            self._callbacks.append(ActionDescriptor(action, predicate))

        log.info("Registering action '%s' OK [%s].",
                 MessageQueue.get_fqcn(action),
                 len(self._callbacks))

        return True

    def unregister(self, action: Callable[[MessageBase], None]) -> bool:
        """Unregisters a callback on the message queue

        Calling the method with the same action twice will return False.

        Returns:
            bool: True, if the action was sucessfully unregistered; false,
                otherwise.
        """

        assert action and callable(action)

        result = False

        with self._sync_root:

            for i, item in enumerate(self._callbacks):

                if item.action is not action:
                    continue

                del self._callbacks[i]
                result = True
                break

        return result

    def __len__(self) -> int:
        """Returns the length of the queue."""
        return len(self._queue_high) + len(self._queue_default)
