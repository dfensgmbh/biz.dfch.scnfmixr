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

from biz.dfch.logging import log

from ..public.ui.streamdeck_type import StreamdeckType
from ..public.input import KeyboardEventMap
from .event_handler_base import EventHandlerBase

from ..system import MessageQueue
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage


class StreamdeckHandler(EventHandlerBase):
    """
    Handles StreamdeckHandler input (Hi2).
    """

    _WAIT_INTERVAL_MS: int = 500
    _EVTEST_FULLNAME = "/usr/bin/evtest"
    _EVTEST_OPTION_GRAB = "--grab"

    _pattern = re.compile(
        r"type 1 \(EV_KEY\), code ([^ ]+) \(([^)]+)\), value 1$"
    )

    _is_disposed: bool
    _is_paused: bool
    _thread: Thread

    _product_id: int
    _device_id: str

    def _on_message(self, message: MessageBase) -> None:
        """This method processes messages."""

        if not isinstance(message, MessageBase):
            return

        if isinstance(
                message, SystemMessage.StateMachine.StateMachineStateEnter):
            return self._on_state_enter(message)

        if isinstance(message, SystemMessage.Shutdown):
            return self._on_shutdown(message)

    def _on_state_enter(self, message: MessageBase) -> None:
        """State enter messages."""

        if not isinstance(
                message, SystemMessage.StateMachine.StateMachineStateEnter):
            return

    def _on_shutdown(self, message: MessageBase) -> None:
        """SystemShutdown."""

        if not isinstance(message, SystemMessage.Shutdown):
            return

        log.debug("on_shutdown: Stopping ...")

        self.dispose()

        log.debug("on_shutdown: Stopping COMPLETED.")

    def __init__(self, type_: StreamdeckType, id_: str):

        super().__init__()

        assert isinstance(type_, StreamdeckType)
        # At this time, only ORIGINAL_MK2 is good.
        assert StreamdeckType.ORIGINAL_MK2 == type_
        assert id_ and id_.strip()

        self._device_id = id_
        self._product_id = type_.value

        self._is_disposed = False
        self._is_paused = False
        self._thread = Thread(target=self._worker, daemon=True)

        MessageQueue.Factory.get().register(
            self._on_message,
            lambda e: isinstance(e, (
                SystemMessage.StateMachine.StateMachineStateEnter,
                SystemMessage.Shutdown)))

    def dispose(self):
        """Dispose method for stopping child process `evtest`."""
        if self._is_disposed:
            return

        self.stop()
        self._is_disposed = True
        self._device_id = ""
        self._product_id = 0x0000

    def _worker(self) -> None:

        log.debug("Initializing _worker ...")
        log.info("Initializing _worker OK.")

        while not self.stop_processing.is_set():

            try:
                pass

                # translated = self._translate(key)

                # log.debug("Code: '%s'. Key: '%s'. Translated: '%s'.",
                #           code, key, translated)

                # self.queue.publish(SystemMessage.InputEvent(translated))

            except Exception as ex:  # pylint: disable=W0718
                log.error("An error occurred. [%s]", ex, exc_info=True)

            finally:
                time.sleep(self._WAIT_INTERVAL_MS / 1000)

        log.info("Stopping worker OK.")

    def _translate(self, key: str, default: str = "") -> str:

        assert key and key.strip()

        result = default

        if key not in KeyboardEventMap.__members__:
            return default

        result = KeyboardEventMap[key].value

        return result

    def start(self) -> bool:
        """Starts the Streamdeck handler."""

        with self.sync_root:

            self.stop_processing.clear()
            self._is_paused = False

            # DFTODO: Add these steps:
            # * Detect Streamdeck
            # * Load images
            # * Convert images

            # cmd: list[str] = [
            #     self._EVTEST_FULLNAME,
            #     self._EVTEST_OPTION_GRAB,
            #     self._device,
            # ]

            # self._process = Process.start(
            #     cmd, wait_on_completion=False, capture_stdout=True)
            # self._thread.start()

    def stop(self) -> bool:
        """Stops the Streamdeck handler."""

        with self.sync_root:
            self.stop_processing.set()
            self._is_paused = False

        return True
