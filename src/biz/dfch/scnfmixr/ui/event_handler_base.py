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

"""Module defining the abstract base class input handling."""

from abc import ABC, abstractmethod
from threading import Event, Lock

from biz.dfch.asyn import ConcurrentQueueT


class EventHandlerBase(ABC):
    """Defines the abstract base class for input handling.

    Attributes:
        stop_processing (Event): Signalled when stop is invoked.
        sync_root (Lock): A non-reentrant lock for synchronisation.
        queue (ConcurrentQueueT[str]): The event queue to be fed by the
            event handler.
    """

    stop_processing: Event
    sync_root: Lock
    queue: ConcurrentQueueT[str]
    _is_paused: bool

    def __init__(self, queue: ConcurrentQueueT[str]):

        super().__init__()

        assert queue

        self.stop_processing = Event()
        self.sync_root = Lock()
        self.queue = queue
        self._is_paused = False

    @abstractmethod
    def start(self):
        """
        Return:
            bool: True, if successful, false otherwise.
        """

        return False

    @abstractmethod
    def stop(self):
        """
        Return:
            bool: True, if successful, false otherwise.
        """

        return False

    @property
    def is_started(self) -> bool:
        """Determines whether keyboard processing is active or not.

        Returns:
            bool: True, if processing is started; false, otherwise.
        """

        return not self.stop_processing.is_set()

    @property
    def is_paused(self) -> bool:
        """Determines whether keyboard processing is paused or not.

        Returns:
            bool: True, if processing is paused; false, otherwise.
        """

        return not self.stop_processing.is_set()

    def pause(self) -> bool:
        """Pauses keyboard processing.

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
        """Resumes keyboard processing.

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
