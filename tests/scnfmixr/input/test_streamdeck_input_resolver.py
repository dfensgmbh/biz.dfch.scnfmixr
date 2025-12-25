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
from biz.dfch.scnfmixr.public.input.streamdeck_event_map import (
    StreamdeckEventMap
)
from biz.dfch.scnfmixr.public.input.streamdeck_input import (
    StreamdeckInput
)
from biz.dfch.scnfmixr.public.input.input_event_map import (
    InputEventMap
)


class TestStreamdeckInputResolver(unittest.TestCase):
    """TestStreamdeckInputResolver"""

    def test_resolve_invalid_state_and_key_returns_none(self):

        sut = StreamdeckInputResolver()

        key = StreamdeckInput(1)
        name = "invalid-state"

        result = sut.invoke(name, key)

        self.assertEqual(None, result)

    def test_resolve_valid_state_and_key_returns_valid_input_event_map(self):

        sut = StreamdeckInputResolver()

        key = StreamdeckInput(1)
        name = "Main"
        expected = InputEventMap.KEY_1

        result = sut.invoke(name, key)

        self.assertEqual(expected, result)

    def test_translate_with_enter_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_ENTER
        expected = "ENTER"

        result = sut.translate(event)

        self.assertEqual(expected, result)

    def test_translate_with_backspace_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_BACKSPACE
        expected = "DELETE"

        result = sut.translate(event)

        self.assertEqual(expected, result)

    def test_translate_with_tab_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_TAB
        expected = "TAB"

        result = sut.translate(event)

        self.assertEqual(expected, result)

    def test_translate_with_1_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_1
        expected = "1"

        result = sut.translate(event)

        self.assertEqual(expected, result)

    def test_translate_with_asterisk_succeeds(self):

        sut = StreamdeckInputResolver()

        event = InputEventMap.KEY_ASTERISK
        expected = "*"

        result = sut.translate(event)

        self.assertEqual(expected, result)

    def test_translate_with_invalid_input_throws(self):

        sut = StreamdeckInputResolver()

        event = "-1"  # invalid input event

        with self.assertRaises(AssertionError):
            _ = sut.translate(event)

    def test_translate_with_none_input_throws(self):

        sut = StreamdeckInputResolver()

        event = None  # invalid input event

        with self.assertRaises(AssertionError):
            _ = sut.translate(event)

    def test_invalid_state_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "invalid-state-name"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.FR

        expected = "res/img/FR/default.png"

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_missing_key_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "Main"
        key = StreamdeckInput.KEY_0E
        code = LanguageCode.IT

        expected = "res/img/IT/Main-default.png"

        _ = StreamdeckEventMap["Main"].pop(StreamdeckInput.KEY_0E)
        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_valid_key_missing_image_returns_default(self):

        sut = StreamdeckInputResolver()

        state = "Main"
        key = StreamdeckInput.KEY_01
        code = LanguageCode.EN

        expected = "res/img/EN/Main-default.png"

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))

    def test_valid_state_valid_key_existing_image_succeeds(self):

        sut = StreamdeckInputResolver()

        state = "Main"
        key = StreamdeckInput.KEY_00
        code = LanguageCode.EN

        expected = "res/img/EN/Main-KEY_00-VolumeUpBlue.png"

        result = sut.get_input_event_image(state, key, code)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result.as_posix()).endswith(expected), str(result))
