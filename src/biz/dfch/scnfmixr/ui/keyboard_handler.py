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

"""Module defining the class keyboard input handling."""

from __future__ import annotations
import re
from threading import Thread
import time

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from ..public.input import KeyboardEventMap
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..system import MessageQueue

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

    def _on_shutdown(self, message: MessageBase) -> None:
        """SystemShutdown."""

        if not isinstance(message, SystemMessage.Shutdown):
            return

        log.debug("on_shutdown: Stopping ...")

        self.dispose()

        log.debug("on_shutdown: Stopping COMPLETED.")

    def __init__(self, device: str):

        super().__init__()

        assert device and device.strip()

        self._is_disposed = False
        self._is_paused = False
        self._device = device
        self._thread = Thread(target=self._worker, daemon=True)

        MessageQueue.Factory.get().register(
            self._on_shutdown,
            lambda msg: isinstance(msg, SystemMessage.Shutdown)
        )

    def dispose(self):
        """Dispose method for stopping child process `evtest`."""
        if self._is_disposed:
            return

        self.stop()
        self._process = None
        self._is_disposed = True

    def _worker(self) -> None:

        log.debug("Initializing _worker ...")
        log.info("Initializing _worker OK.")

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

                    self.queue.publish(SystemMessage.InputEvent(translated))

            except Exception as ex:  # pylint: disable=W0718
                log.error("An error occurred. [%s]", ex, exc_info=True)

            finally:
                time.sleep(self._WAIT_INTERVAL_MS / 1000)

        log.info("Stopping worker OK.")

    def _translate(self, key: str, default: str = "") -> str:

        assert key and key.strip()
        assert isinstance(default, str)

        result = default

        if key not in KeyboardEventMap.__members__:
            return result

        result = KeyboardEventMap[key].value

        return result

    def start(self) -> bool:
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

        return True

    def stop(self) -> bool:
        """Stops the keyboard handler."""

        with self.sync_root:
            self.stop_processing.set()
            self._is_paused = False
            self._process.stop(force=True)

        return True
