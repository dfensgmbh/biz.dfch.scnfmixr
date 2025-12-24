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

"""Module defining the abstract base class input handling."""

from abc import ABC, abstractmethod
from threading import Event, Lock

from ..system import MessageQueue


class EventHandlerBase(ABC):
    """Defines the abstract base class for input handling.

    Attributes:
        stop_processing (Event): Signalled when stop is invoked.
        sync_root (Lock): A non-reentrant lock for synchronisation.
        queue (MessageQueue): The event queue to be used by the
            event handler.
    """

    stop_processing: Event
    sync_root: Lock
    queue: MessageQueue
    _is_paused: bool

    def __init__(self):

        super().__init__()

        self.stop_processing = Event()
        self.sync_root = Lock()
        self.queue = MessageQueue.Factory.get()
        self._is_paused = False

    @abstractmethod
    def start(self):
        """Starts the handler.

        Return:
            bool: True, if successful; false otherwise.
        """

        return False

    @abstractmethod
    def stop(self):
        """Stops the handler.

        Return:
            bool: True, if successful; false otherwise.
        """

        return False

    @property
    def is_started(self) -> bool:
        """Determines whether input processing is active or not.

        Returns:
            bool: True, if processing is started; false, otherwise.
        """

        return not self.stop_processing.is_set()

    @property
    def is_paused(self) -> bool:
        """Determines whether input processing is paused or not.

        Returns:
            bool: True, if processing is paused; false, otherwise.
        """

        return not self.stop_processing.is_set()

    def pause(self) -> bool:
        """Pauses input processing.

        Returns:
            bool: True, if processing is paused; false, if not or if the
                service is not started.
        """

        with self.sync_root:
            if self.stop_processing.is_set():
                return False

            if self._is_paused:
                return True

            self._is_paused = not self._is_paused
            return self._is_paused

    def resume(self) -> bool:
        """Resumes input processing.

        Returns:
            bool: True, if processing is paused; false, if not or if the
                service is not started.
        """

        with self.sync_root:
            if self.stop_processing.is_set():
                return False

            if not self._is_paused:
                return False

            self._is_paused = not self._is_paused
            return self._is_paused
