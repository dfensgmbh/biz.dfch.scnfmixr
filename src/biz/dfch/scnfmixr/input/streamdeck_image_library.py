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

"""StreamdeckImageLibrary class."""

from __future__ import annotations

from threading import Lock
from typing import ClassVar

from StreamDeck.Devices.StreamDeck import StreamDeck  # type: ignore

from biz.dfch.i18n.language_code import LanguageCode
from biz.dfch.logging.log import log

from ...asyn.thread_pool import ThreadPool

from ..public.input.streamdeck_input import StreamdeckInput
from .streamdeck_image_converter import StreamdeckImageConverter
from ..public.input.streamdeck_event_map import StreamdeckEventMap


# pylint: disable=R0903
class StreamdeckImageLibrary:
    """
    This class has all images for each state (pushed, not pushed).
    """

    _images: dict[str, bytes]
    _cache: dict[str, dict[tuple[StreamdeckInput, bool], str]]
    _sync_root: Lock

    _converter: StreamdeckImageConverter

    def __init__(
        self,
        deck: StreamDeck,
        code: LanguageCode,
    ):

        if not type(self).Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert isinstance(deck, StreamDeck)
        assert isinstance(code, LanguageCode)

        self._images = {}
        self._cache = {}
        self._sync_root = Lock()

        self._converter = StreamdeckImageConverter(deck, code)

    def _worker(self, state: str) -> dict[tuple[StreamdeckInput, bool], bytes]:
        """Retrieves all images for a given state."""

        result: dict[tuple[StreamdeckInput, bool], bytes] = {}

        if state in self._cache:
            for key, hash_key in self._cache[state].items():
                result[key] = self._images[hash_key]
            return result

        log.debug("Try to get key and information for '%s' ...", state)

        with self._sync_root:
            if state in self._cache:
                for key, hash_key in self._cache[state].items():
                    result[key] = self._images[hash_key]
                return result

            image_key_map: dict[tuple[StreamdeckInput, bool], str] = {}

            for key in StreamdeckEventMap[state]:
                log.debug("%s: [key %s]", state, key)

                image_normal = self._converter.get_image(state, key)
                hash_normal = self._converter.get_hash_key(image_normal)
                if hash_normal not in self._images:
                    self._images[hash_normal] = image_normal
                image_key_map[(key, False)] = hash_normal

                image_pushed = self._converter.get_image_pushed(state, key)
                hash_pushed = self._converter.get_hash_key(image_pushed)
                if hash_pushed not in self._images:
                    self._images[hash_pushed] = image_pushed
                image_key_map[(key, True)] = hash_pushed

            self._cache[state] = image_key_map

        log.info("Try to get key and information for '%s' SUCCEEDED.", state)

        for key, hash_key in self._cache[state].items():
            result[key] = self._images[hash_key]

        return result

    def get_key_images(
        self,
        state: str
    ) -> dict[tuple[StreamdeckInput, bool], bytes]:
        """Gets the keys for the specified state."""

        assert isinstance(state, str) and state.strip()

        result = self._worker(state)

        return result

    class Factory:  # pylint: disable=R0903
        """Factory."""

        __instance: ClassVar[StreamdeckImageLibrary | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get(
            deck: StreamDeck,
            code: LanguageCode,
        ) -> StreamdeckImageLibrary:
            """Creates or gets a singleton."""

            if StreamdeckImageLibrary.Factory.__instance is not None:
                return StreamdeckImageLibrary.Factory.__instance

            with StreamdeckImageLibrary.Factory._sync_root:

                if StreamdeckImageLibrary.Factory.__instance is not None:
                    return StreamdeckImageLibrary.Factory.__instance

                StreamdeckImageLibrary.Factory.__instance = (
                    StreamdeckImageLibrary(deck=deck, code=code))

            return StreamdeckImageLibrary.Factory.__instance
