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

from biz.dfch.scnfmixr.input.streamdeck_image_library import (
    StreamdeckImageLibrary
)
from biz.dfch.scnfmixr.public.input.streamdeck_event_map import (
    StreamdeckEventMap
)
from biz.dfch.scnfmixr.public.input.streamdeck_input import StreamdeckInput


class TestStreamdeckImageLibrary(unittest.TestCase):
    """TestStreamdeckImageLibrary"""

    def test_private_ctor_throws(self):

        with self.assertRaises(RuntimeError):
            _ = StreamdeckImageLibrary(None, None)

    def test_singleton(self):

        device = Dummy()
        deck = StreamDeckOriginalV2(device)
        code = LanguageCode.EN

        with self.assertRaises(AttributeError) as exc:
            sut = StreamdeckImageLibrary.Factory.get(deck, code)

            other = StreamdeckImageLibrary.Factory.get(deck, code)

            # This statement will raise an `AttributeError`.
            # `Dummy` does not implement `.close()`.
            deck.close()

        self.assertEqual("close", exc.exception.name)

        self.assertEqual(sut, other)

    def test_library(self):

        device = Dummy()
        deck = StreamDeckOriginalV2(device)
        code = LanguageCode.EN

        state = "Main"

        with self.assertRaises(AttributeError) as exc:
            sut = StreamdeckImageLibrary.Factory.get(deck, code)

            result = sut.get_key_information(state)

            # This statement will raise an `AttributeError`.
            # `Dummy` does not implement `.close()`.
            deck.close()

        self.assertEqual("close", exc.exception.name)

        self.assertTrue((StreamdeckInput.KEY_00, False) in result)
        self.assertTrue((StreamdeckInput.KEY_00, True) in result)

        for key, value in StreamdeckEventMap.items():
            result = sut.get_key_information(key)

            for input_ in value:
                self.assertTrue((input_, True) in result)
