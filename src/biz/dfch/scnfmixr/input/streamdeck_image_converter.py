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

"""StreamdeckImageConverter class."""

from __future__ import annotations


from hashlib import blake2b
from pathlib import Path
from typing import ClassVar

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.Devices.StreamDeck import StreamDeck  # type: ignore
from StreamDeck.ImageHelpers import PILHelper  # type: ignore

from biz.dfch.i18n.i18n import I18n
from biz.dfch.i18n.language_code import LanguageCode
from biz.dfch.logging.log import log

from ..public.input.streamdeck_input import StreamdeckInput
from .streamdeck_input_resolver import StreamdeckInputResolver


class StreamdeckImageConverter:
    """
    Converts images to native stream deck format.
    """

    # Font, font size and margin must agree with each other.
    SIZE: int = 12
    MARGIN_BOTTOM: int = 16

    FONT_NAME = "Roboto-Regular.ttf"

    COLOR: str = "white"

    _font: ClassVar[ImageFont.FreeTypeFont | None] = None

    _deck: StreamDeck
    _code: LanguageCode

    def __init__(
        self,
        deck: StreamDeck,
        code: LanguageCode = LanguageCode.DEFAULT
    ):

        # For reasons, that I do not know, the assertion fails,
        # because `deck` is not of type `StreamDeck`.
        # During test, with `Dummy` it is ...
        # assert isinstance(deck, StreamDeck)
        assert isinstance(code, LanguageCode)

        self._deck = deck
        self._code = code

        # Get the font only once.
        if type(self)._font is None:

            log.debug("Try to get location of font name '%s' ...",
                      self.FONT_NAME)
            font = Path(I18n.Factory.get().get_resource_path(self.FONT_NAME))
            assert isinstance(font, Path) and font.exists()

            log.debug("Try to get font name '%s' from location '%s' ...",
                      self.FONT_NAME, font)
            type(self)._font = ImageFont.truetype(
                font, self.SIZE)
            log.info("Try to get font name '%s' from location '%s' SUCCEEDED.",
                     self.FONT_NAME, font)

    def get_image(
        self,
        state: str,
        key: StreamdeckInput,
    ) -> bytes:
        """
        The method does these steps. It:
            * Loads the image
            * Scales the image
            * Applies the label text to the image
            * Returns the image in `bytes`.
        """

        return self._get_image(
            state=state,
            key=key,
            margins=(0, 0, self.MARGIN_BOTTOM, 0),
            has_text=True
        )

    def get_image_pushed(
        self,
        state: str,
        key: StreamdeckInput,
    ) -> bytes:
        """
        The method does these steps. It:
            * Loads the image
            * Scales the image to a "pushed" (smaller) size
            * Returns the image in `bytes`.
        """

        return self._get_image(
            state=state,
            key=key,
            margins=(8, 8, 8, 8),
            has_text=False
        )

    # pylint: disable=R0913
    # pylint: disable=R0917
    def _get_image(
        self,
        state: str,
        key: StreamdeckInput,
        margins: tuple[int, int, int, int],
        has_text: bool = True,
        color: str | None = None,
    ) -> bytes:

        assert isinstance(state, str)
        assert isinstance(key, StreamdeckInput)
        assert isinstance(margins, tuple)
        assert len(margins) == 4
        assert all(isinstance(m, int) for m in margins)

        if color is None:
            color = self.COLOR
        assert color.strip()

        resolver = StreamdeckInputResolver()
        log.debug(
            "Try to get image for '%s:%s' [%s] ...",
            state, key.name,
            self._code)
        image_path = resolver.get_input_event_image(state, key, self._code)
        assert Path(image_path).exists
        log.info(
            "Try to get image for '%s:%s' [%s] SUCCEEDED: '%s'.",
            state,
            key.name,
            self._code, image_path
        )

        log.debug("Try to open image '%s' ...", image_path)
        image_file = Image.open(image_path)
        log.info("Try to open image '%s' SUCCEEDED.", image_path)

        log.debug("Try to change size of image '%s' ...", image_path)
        scaled_image = PILHelper.create_scaled_key_image(
            self._deck, image_file, margins=margins)
        log.info("Try to change size of image '%s' SUCCEEDED.", image_path)

        if not has_text:
            result = PILHelper.to_native_key_format(self._deck, scaled_image)
            return result

        log.debug("Try to get text for '%s:%s' ...", state, key.name)
        input_event = resolver.invoke(state, key)
        text = resolver.translate(input_event, code=self._code)
        log.info("Try to get text for '%s:%s' SUCCEEDED: '%s'.",
                 state, key.name, text)

        log.debug("Try to write text '%s' onto image '%s' ...",
                  text,
                  image_path)
        draw = ImageDraw.Draw(scaled_image)
        draw.text(
            (scaled_image.width / 2, scaled_image.height - 5),
            text=text,
            font=self._font,
            anchor="ms",
            fill=color
        )
        log.info("Try to write text '%s' onto image '%s' SUCCEEDED.",
                 text, image_path)

        result = PILHelper.to_native_key_format(self._deck, scaled_image)

        return result

    def get_hash_key(self, image: bytes) -> str:
        """Makes the hexadecimal hash key from a given image.

        Args:
            image(bytes):
                The image, that we use to create a hex hash key from.

        Returns:
            out(bytes):
                The hash key as a hexadecimal string.
        """

        assert isinstance(image, bytes)

        # This is equivalent to SHA256.
        digest_size = 32
        hash_alg = blake2b(image, digest_size=digest_size)

        result = hash_alg.hexdigest()

        return result
