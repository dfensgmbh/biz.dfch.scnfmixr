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
from ..input.streamdeck_input_resolver import StreamdeckInputResolver


class StreamdeckHandler(EventHandlerBase):
    """
    Handles StreamdeckHandler input (Hi2).
    """

    _WAIT_INTERVAL_MS: int = 500
    _CODE: LanguageCode = LanguageCode.EN

    _is_disposed: bool

    _mq: MessageQueue
    _deck: StreamDeckOriginalV2
    _resolver: StreamdeckInputResolver
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
            return  # NOSONAR python:S3626

    def _on_state_enter(self, message: MessageBase) -> None:
        """StateMachine enter messages."""

        if not isinstance(
                message, SystemMessage.StateMachine.StateMachineStateEnter):
            return

        message = cast(
            SystemMessage.StateMachine.StateMachineStateEnter, message)
        self._current_state = message.value
        log.debug("_on_state_enter: '%s'.", self._current_state)

        # When we try to set all images to black with "set_key_color()",
        # not all images will be set to black. We do not know why.
        # Thus, we "reset()" the deck. This shows the boot screen momentarily.
        self._deck.reset()

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

        # We start with an empty initial state and
        # wait for the first update event.
        self._current_state = ""

        # Select the correct Streamdeck.
        idx = int(index)
        decks = DeviceManager().enumerate()
        assert len(decks) > idx
        self._deck = decks[idx]

        assert isinstance(self._deck, StreamDeck)

        # Subscribe to message queue.
        self._mq = MessageQueue.Factory.get()
        self._mq.register(
            self._on_message,
            lambda e: isinstance(e, (
                SystemMessage.StateMachine.StateMachineStateEnter,
                SystemMessage.Shutdown)))

        # Initialize image library and resolver.
        self._resolver = StreamdeckInputResolver()
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

        if not self._current_state.strip():
            log.warning("_callback: _current_state is invalid.")
            return

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
            if key_image_map is None:
                log.warning(
                    "_callback: No key_image_map for state '%s' found.",
                    self._current_state)
                return

            mapping_key = (key, deck_key_state)
            image_bytes = key_image_map.get(mapping_key)
            if image_bytes is None:
                log.warning(
                    "_callback: No image for state '%s' "
                    "and key '%s' [state: %s] found.",
                    self._current_state,
                    key,
                    deck_key_state)
                return

            self._deck.set_key_image(deck_key, image_bytes)

            # Only process key presses for key up events.
            if deck_key_state:
                return

            # Translate streamdeck key to input event.
            input_event = self._resolver.resolve(self._current_state, key)
            translated = input_event.value
            log.debug(
                "State: '%s'. Key: '%s'. Translated: '%s'.",
                self._current_state,
                key,
                translated)
            self._mq.publish(SystemMessage.InputEvent(translated))

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
