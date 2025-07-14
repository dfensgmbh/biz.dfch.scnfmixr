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

"""Module app_notification."""

from __future__ import annotations
from threading import Event
from threading import Lock
from threading import Thread
from typing import ClassVar
from typing import Callable
from enum import Enum, auto

from biz.dfch.logging import log


__all__ = [
    "AppNotification",
]


class AppNotification:  # pylint: disable=R0903
    """Handles application wide notifications."""

    class Event(Enum):
        """Notification types."""

        SHUTDOWN = auto()

    _sync_root: Lock
    _callbacks: list[Callable[[Event], None]]
    _signal: Event

    def __init__(self):
        """Private ctor. Use Factory to create an instance of this object."""

        if not AppNotification.Factory._lock.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        self._sync_root = Lock()
        self._callbacks = []
        self._signal = Event()

    def register(self, action: Callable[[Event], None]) -> None:
        """Registers action.

        Args:
            action (Callable[[Event], None]): The action to register.
        Returns:
            None:
        """

        assert action and callable(action)

        log.debug("Registering action '%s' ...", action)

        with self._sync_root:
            self._callbacks.append(action)

        log.info("Registering action '%s' COMPLETED.", action)

    def signal(self, event: AppNotification.Event) -> None:
        """Signals the specified event to all registered actions.

        Args:
            event (Event): The event to signal.

        Returns:
            None:
        """

        assert event is not None and isinstance(event, AppNotification.Event)

        def dispatch(event: AppNotification.Event) -> None:
            """Dispatcher for event notificiations."""

            with self._sync_root:
                actions = list(self._callbacks)

            count = len(actions)
            for index, action in enumerate(actions):

                try:
                    log.debug(
                        ("Dispatching event '%s' to action '%s' .... "
                         "[%s/%s]"),
                        event, action,
                        index+1, count)

                    action(event)

                    log.info(
                        ("Dispatching event '%s' to action '%s' SUCCEEDED. "
                         "[%s/%s]"),
                        event, action,
                        index+1, count)

                except Exception:  # pylint: disable=W0718
                    log.error(
                        ("Dispatching event '%s' to action '%s' FAILED. "
                         "[%s/%s]"),
                        event, action,
                        index+1, count,
                        exc_info=True)

        if AppNotification.Event.SHUTDOWN != event:
            Thread(target=dispatch, args=(event,), daemon=True).start()
            return

        dispatch(event)

    def signal_shutdown(self) -> None:
        """Signals a SHUTDOWN event."""
        self.signal(AppNotification.Event.SHUTDOWN)

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AppNotification] = None
        _lock: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> AppNotification:
            """Returns the singleton instance."""

            if AppNotification.Factory.__instance is not None:
                return AppNotification.Factory.__instance

            with AppNotification.Factory._lock:

                if AppNotification.Factory.__instance is not None:
                    return AppNotification.Factory.__instance

                AppNotification.Factory.__instance = AppNotification()

            return AppNotification.Factory.__instance
