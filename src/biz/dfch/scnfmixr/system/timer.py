# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

"""timer"""

import threading
from typing import Callable


class Timer:
    """
    Thread that waits the specified amount of time and then invokes a callback.
    """

    _timer: threading.Timer | None
    _callback: Callable[[], None] | None
    _lock: threading.Lock

    delay_seconds: float

    def __init__(self, timeout_seconds: float) -> None:
        self.delay_seconds: float = timeout_seconds
        self._timer: threading.Timer | None = None
        self._callback: Callable[[], None] | None = None
        self._lock: threading.Lock = threading.Lock()

    def start(self, callback: Callable[[], None]) -> None:
        """
        Start the timer. Invoke callback after specified timeout.
        """

        with self._lock:
            if self._timer is not None:
                return  # Timer already running

            self._callback = callback
            self._timer = threading.Timer(
                self.delay_seconds, self._invoke)
            self._timer.start()

    def _invoke(self) -> None:
        """
        Internal method called when timer expires.
        """

        if self._callback:
            self._callback()

    def cancel(self) -> None:
        """
        Cancel the shutdown timer.
        """

        with self._lock:
            if not self._timer:
                return

            self._timer.cancel()
            self._timer = None
