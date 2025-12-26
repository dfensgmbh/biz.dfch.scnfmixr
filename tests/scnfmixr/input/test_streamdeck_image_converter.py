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

"""TestStreamdeckImageConverter class"""

# pylint: disable=missing-function-docstring

import unittest

from StreamDeck.Devices.StreamDeckOriginalV2 import (  # type: ignore
    StreamDeckOriginalV2)
from StreamDeck.Transport.Dummy import (  # type: ignore
    Dummy)

from biz.dfch.i18n.language_code import LanguageCode

from biz.dfch.scnfmixr.input.streamdeck_image_converter import (
    StreamdeckImageConverter
)
from biz.dfch.scnfmixr.public.input.streamdeck_event_map import (
    StreamdeckEventMap,
    _streamdeck_event_map_default
)
from biz.dfch.scnfmixr.public.input.streamdeck_input import (
    StreamdeckInput
)


class TestStreamdeckImageConverter(unittest.TestCase):
    """TestStreamdeckImageConverter"""

    def test_get_image_and_get_hash_key_succeeds(self):

        state = "Test"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.DEFAULT
        expected = (
            "9d3eb4213ad0af309239f0e8a081b5be"
            "4fc3843b9169f589cae681d28d03f0b0"
        )

        # pylint: disable=W0212
        StreamdeckEventMap[state] = _streamdeck_event_map_default

        with self.assertRaises(AttributeError) as exc:

            device = Dummy()
            deck = StreamDeckOriginalV2(device)

            sut = StreamdeckImageConverter(deck, code)

            image_bytes = sut.get_image(state, key)
            result = sut.get_hash_key(image_bytes)

            self.assertEqual(expected, result)

            # This statement will raise an `AttributeError`.
            # `Dummy` does not implement `.close()`.
            deck.close()

        self.assertEqual("close", exc.exception.name)

    def test_get_image_pressed_and_get_hash_key_succeeds(self):

        name = "Test"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.DEFAULT
        expected = (
            "9f450360d771e694d7ed39317c72fd9c"
            "914ca4d56702cf08091c89087525aac1"
        )

        # pylint: disable=W0212
        StreamdeckEventMap[name] = _streamdeck_event_map_default

        with self.assertRaises(AttributeError) as exc:

            device = Dummy()
            deck = StreamDeckOriginalV2(device)

            sut = StreamdeckImageConverter(deck, code)

            image_bytes = sut.get_image_pressed(name, key)
            result = sut.get_hash_key(image_bytes)

            self.assertEqual(expected, result)

            # This statement will raise an `AttributeError`.
            # `Dummy` does not implement `.close()`.
            deck.close()

        self.assertEqual("close", exc.exception.name)
