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

"""Module defining the class keyboard input handling."""

from __future__ import annotations
import re
from threading import Thread
import time

from biz.dfch.asyn import Process, ConcurrentQueueT
from biz.dfch.logging import log

from ..app import ApplicationContext
from ..notifications import AppNotification
from ..public.input import KeyboardEventMap
from .event_handler_base import EventHandlerBase


class KeyboardHandler(EventHandlerBase):
    """Handles keyboard input (Hi1).

    Internally, it uses `evtest` for reading keyboard scan codes (and not
    actual keys ike 'A').
    """

    _WAIT_INTERVAL_MS: int = 500
    _EVTEST_FULLNAME = "/usr/bin/evtest"
    _EVTEST_OPTION_GRAB = "--grab"

    _pattern = re.compile(
        r"type 1 \(EV_KEY\), code ([^ ]+) \(([^)]+)\), value 1$"
    )

    _is_disposed: bool
    _is_paused: bool
    _device: str
    _thread: Thread
    _process: Process

    def on_shutdown(self, event: AppNotification.Event) -> None:
        """Process SHUTDOWN notification."""

        if event is None or AppNotification.Event.SHUTDOWN != event:
            return

        log.debug("on_shutdown: Stopping ...")

        self.dispose()

        log.debug("on_shutdown: Stopping COMPLETED.")

    def __init__(self, queue: ConcurrentQueueT[str], device: str):

        super().__init__(queue)

        assert device and device.strip()

        self._is_disposed = False
        self._is_paused = False
        self._device = device
        self._thread = Thread(target=self._worker, daemon=True)

        ApplicationContext.Factory.get().notification.register(self.on_shutdown)

    def dispose(self):
        """Dispose method for stopping child process `evtest`."""
        if self._is_disposed:
            return

        self.stop()
        self._process = None
        self._is_disposed = True

    def _worker(self) -> None:

        log.debug("Starting worker ...")

        while not self.stop_processing.is_set():

            try:
                if not self._process or not self._process.is_running:
                    continue

                for line in self._process.stdout:

                    if self._is_paused:
                        continue

                    result = self._pattern.search(line)
                    if not result:
                        continue

                    code = result.group(1)
                    key = result.group(2)

                    translated = self._translate(key)

                    log.debug("Code: '%s'. Key: '%s'. Translated: '%s'.",
                              code, key, translated)

                    self.queue.enqueue(translated)

            except Exception as ex:  # pylint: disable=W0718
                log.error("An error occurred. [%s]", ex, exc_info=True)

            finally:
                time.sleep(self._WAIT_INTERVAL_MS / 1000)

        log.debug("Stopping worker ...")

    def _translate(self, key: str, default: str = "") -> str:

        assert key and key.strip()

        result = default

        if key not in KeyboardEventMap.__members__:
            return default

        result = KeyboardEventMap[key].value

        return result

    def start(self):
        """Starts the keyboard handler."""

        with self.sync_root:

            self.stop_processing.clear()
            self._is_paused = False

            cmd: list[str] = [
                self._EVTEST_FULLNAME,
                self._EVTEST_OPTION_GRAB,
                self._device,
            ]

            self._process = Process.start(
                cmd, wait_on_completion=False, capture_stdout=True)
            self._thread.start()

    def stop(self) -> None:
        """Stops the keyboard handler."""

        with self.sync_root:
            self.stop_processing.set()
            self._is_paused = False
            self._process.stop(force=True)
