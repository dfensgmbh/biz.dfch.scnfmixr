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
from typing import cast

from StreamDeck.DeviceManager import DeviceManager  # type: ignore
from StreamDeck.Devices.StreamDeck import StreamDeck  # type: ignore
from StreamDeck.Devices.StreamDeckOriginalV2 import (  # type: ignore
    StreamDeckOriginalV2
)

from biz.dfch.logging import log
from biz.dfch.i18n.language_code import LanguageCode

from ..public.input import StreamdeckInput
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..system import MessageQueue

from .event_handler_base import EventHandlerBase

from ..input.streamdeck_image_library import StreamdeckImageLibrary


class StreamdeckHandler(EventHandlerBase):
    """
    Handles StreamdeckHandler input (Hi2).
    """

    _WAIT_INTERVAL_MS: int = 500
    _CODE: LanguageCode = LanguageCode.EN

    _is_disposed: bool

    _deck: StreamDeckOriginalV2
    _library = StreamdeckImageLibrary

    _current_state: str

    def _on_message(self, message: MessageBase) -> None:
        """This method processes messages."""

        if not isinstance(message, MessageBase):
            return

        if isinstance(
                message, SystemMessage.StateMachine.StateMachineStateEnter):
            self._on_state_enter(message)
            return

        if isinstance(message, SystemMessage.Shutdown):
            self._on_shutdown(message)
            return

    def _on_state_enter(self, message: MessageBase) -> None:
        """StateMachine enter messages."""

        if not isinstance(
                message, SystemMessage.StateMachine.StateMachineStateEnter):
            return

        message = cast(
            SystemMessage.StateMachine.StateMachineStateEnter, message)
        self._current_state = message.value
        log.debug("_on_state_enter: '%s'.", self._current_state)

        self._deck.reset()
        # for key in StreamdeckInput:
        #     self._deck.set_key_color(key, 0, 0, 0)

        # Show all images of current screen.
        key_image_map = self._library.get_key_images(self._current_state)
        assert key_image_map is not None
        for k, image_bytes in key_image_map.items():
            key, state = k
            if not state:
                self._deck.set_key_image(key, image_bytes)

    def _on_shutdown(self, message: MessageBase) -> None:
        """SystemShutdown."""

        if not isinstance(message, SystemMessage.Shutdown):
            return

        log.debug("on_shutdown: Stopping ...")

        self.dispose()

        log.debug("on_shutdown: Stopping COMPLETED.")

    def __init__(self, index: str):

        super().__init__()

        assert index and index.strip()

        self._is_disposed = False

        # This is the initial state.
        # DFTODO: Maybe we can leave it "", and wait for the first state
        # change message.
        self._current_state = "InitialiseLcl"

        # Select the correct Streamdeck.
        idx = int(index)
        decks = DeviceManager().enumerate()
        assert len(decks) > idx
        self._deck = decks[idx]
        # for i, deck in enumerate(decks):
        #     if i != idx:
        #         continue

        #     self._deck = deck
        #     break

        assert isinstance(self._deck, StreamDeck)

        # Subscribe to message queue.
        MessageQueue.Factory.get().register(
            self._on_message,
            lambda e: isinstance(e, (
                SystemMessage.StateMachine.StateMachineStateEnter,
                SystemMessage.Shutdown)))

        # Initialize image library.
        self._library = StreamdeckImageLibrary.Factory.get(
            self._deck, self._CODE)

    def dispose(self):
        """Dispose method for stopping child process `evtest`."""
        if self._is_disposed:
            return

        self.stop()
        self._is_disposed = True

    def _callback(
        self,
        deck: StreamDeck,
        deck_key: int,
        deck_key_state: bool
    ) -> None:

        log.debug("_callback: state: '%s'. key '%s'. key_state '%s'.",
                  self._current_state, deck_key, deck_key_state)

        if deck is None or not isinstance(deck, StreamDeck):
            log.warning("_callback: deck is invalid.")
            return

        if deck_key is None or not isinstance(deck_key, int):
            log.warning("_callback: deck_key is invalid.")
            return

        try:
            key = StreamdeckInput(deck_key)
            key_image_map = self._library.get_key_images(
                state=self._current_state)
            assert key_image_map is not None

            dict_key = (key, deck_key_state)
            image_bytes = key_image_map[dict_key]
            assert image_bytes is not None and 0 < len(image_bytes)

            self._deck.set_key_image(deck_key, image_bytes)

        except Exception as ex:  # pylint: disable=W0718
            log.error("An error occurred. [%s]", ex, exc_info=True)

    def start(self) -> bool:
        """Starts the Streamdeck handler."""

        log.debug("%s: Try to start handler ...", type(self).__name__)
        try:
            with self.sync_root:
                self._deck.open()
                self._deck.reset()
                self._deck.set_brightness(30)
                self._deck.set_key_callback(self._callback)

            log.info("%s: Try to start handler SUCCEEDED.", type(self).__name__)
            return True

        except Exception as ex:  # pylint: disable=W0718
            log.error("An error occurred. [%s]", ex, exc_info=True)
            return False

    def stop(self) -> bool:
        """Stops the Streamdeck handler."""

        log.debug("%s: Try to stop handler ...", type(self).__name__)
        with self.sync_root:

            with self._deck:
                self._deck.reset()
                self._deck.close()

        log.info("%s: Try to stop handler SUCCEEDED.", type(self).__name__)
        return True
