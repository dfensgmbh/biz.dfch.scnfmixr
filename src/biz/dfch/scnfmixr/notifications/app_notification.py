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

"""Module app_notification."""

from __future__ import annotations
import threading
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

    _sync_root: threading.Lock
    _callbacks: list[Callable[[threading.Event], None]]

    def __init__(self):
        """Private ctor. Use Factory to create an instance of this object."""

        if not AppNotification.Factory._lock.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        self._sync_root = threading.Lock()
        self._callbacks = []

    def register(self, action: Callable[[threading.Event], None]) -> None:
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
                        ("Dispatching event '%s' to action '%s' OK. "
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
            threading.Thread(target=dispatch, args=(
                event,), daemon=True).start()
            return

        dispatch(event)

    def signal_shutdown(self) -> None:
        """Signals a SHUTDOWN event."""
        self.signal(AppNotification.Event.SHUTDOWN)

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AppNotification] = None
        _lock: ClassVar[threading.Lock] = threading.Lock()

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
