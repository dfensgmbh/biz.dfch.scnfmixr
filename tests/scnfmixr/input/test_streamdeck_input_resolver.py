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

"""TestStreamdeckInputResolver class"""

# pylint: disable=missing-function-docstring

from pathlib import Path
import unittest

from biz.dfch.i18n.language_code import LanguageCode
from biz.dfch.scnfmixr.input.streamdeck_input_resolver import (
    StreamdeckInputResolver
)
from biz.dfch.scnfmixr.public.input.input_event_map import (
    InputEventMap
)
from biz.dfch.scnfmixr.public.input.streamdeck_input import (
    StreamdeckInput
)
from biz.dfch.scnfmixr.public.input.streamdeck_event_map import (
    StreamdeckEventMap,
    _streamdeck_event_map_default
)


class TestStreamdeckInputResolver(unittest.TestCase):
    """TestStreamdeckInputResolver"""

    def test_resolve_invalid_state_and_key_returns_none(self):

        sut = StreamdeckInputResolver()

        key = StreamdeckInput(1)
        name = "invalid-state"

        result = sut.resolve(name, key)

        self.assertEqual(None, result)

    def test_resolve_valid_state_and_key_returns_valid_input_event_map(self):

        sut = StreamdeckInputResolver()

        key = StreamdeckInput(1)
        name = "Main"
        expected = InputEventMap.KEY_1

        result = sut.resolve(name, key)

        self.assertEqual(expected, result)

    def test_get_text_with_enter_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_ENTER
        expected = "ENTER"

        result = sut.get_text(event)

        self.assertEqual(expected, result)

    def test_get_text_with_backspace_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_BACKSPACE
        expected = "DELETE"

        result = sut.get_text(event)

        self.assertEqual(expected, result)

    def test_get_text_with_tab_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_TAB
        expected = "TAB"

        result = sut.get_text(event)

        self.assertEqual(expected, result)

    def test_get_text_with_1_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_1
        expected = "1"

        result = sut.get_text(event)

        self.assertEqual(expected, result)

    def test_get_text_with_asterisk_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_ASTERISK
        expected = "*"

        result = sut.get_text(event)

        self.assertEqual(expected, result)

    def test_get_text_with_invalid_input_throws(self):

        sut = StreamdeckInputResolver()

        event = "-1"  # invalid input event

        with self.assertRaises(AssertionError):
            _ = sut.get_text(event)

    def test_get_text_with_none_input_throws(self):

        sut = StreamdeckInputResolver()

        event = None  # invalid input event

        with self.assertRaises(AssertionError):
            _ = sut.get_text(event)

    def test_invalid_state_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "invalid-state-name"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.FR

        expected = (
            f"res/img/{code.name}/"
            f"default"
            ".png"
        )

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_missing_key_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "Test"
        key = StreamdeckInput.KEY_0E
        code = LanguageCode.IT

        # pylint: disable=W0212
        StreamdeckEventMap[state] = _streamdeck_event_map_default

        expected = (
            f"res/img/{code.name}/"
            f"{state}-default"
            ".png"
        )

        _ = StreamdeckEventMap["Main"].pop(StreamdeckInput.KEY_0E)
        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_valid_key_missing_image_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "Test"
        key = StreamdeckInput.KEY_02
        code = LanguageCode.EN

        # pylint: disable=W0212
        StreamdeckEventMap[state] = _streamdeck_event_map_default

        expected = (
            f"res/img/{code.name}/"
            f"{state}-default"
            ".png"
        )

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_valid_key_existing_image_succeeds(self):

        sut = StreamdeckInputResolver()

        state = "Test"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.EN

        # pylint: disable=W0212
        StreamdeckEventMap[state] = _streamdeck_event_map_default

        expected = (
            f"res/img/{code.name}/"
            f"{state}-{key.name}-VolumeUpBlue"
            ".png"
        )

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))
