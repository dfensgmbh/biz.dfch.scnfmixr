# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

# pylint: disable=C0115
# pylint: disable=C0116

"""test_menu_profile"""

from typing import cast

import unittest

from biz.dfch.scnfmixr.public.input import MenuProfile
from biz.dfch.scnfmixr.public.input import InputDevice

from biz.dfch.scnfmixr.public.input import KeyboardEventMap
from biz.dfch.scnfmixr.public.input import StreamdeckEventMap


class TestMenuProfile(unittest.TestCase):

    def test_resolve_default_hi1(self):

        expected: type = KeyboardEventMap

        sut = MenuProfile.DEFAULT

        result = sut.get_event_map(InputDevice.HI1)

        self.assertEqual(expected, result)

    def test_resolve_default_hi2(self):

        expected: type = StreamdeckEventMap

        sut = MenuProfile.DEFAULT

        result = sut.get_event_map(InputDevice.HI2)

        self.assertEqual(expected, result)

    def test_resolve_default_hi3(self):

        sut = MenuProfile.DEFAULT

        with self.assertRaises(NotImplementedError):
            _ = sut.get_event_map(InputDevice.HI3)

    def test_resolve_recorder_hi1(self):

        expected: type = KeyboardEventMap

        sut = MenuProfile.RECORDER

        result = sut.get_event_map(InputDevice.HI1)

        self.assertEqual(expected, result)

    def test_resolve_recorder_hi2(self):

        expected: type = StreamdeckEventMap

        sut = MenuProfile.RECORDER

        result = sut.get_event_map(InputDevice.HI2)

        self.assertEqual(expected, result)

    def test_resolve_recorder_hi3(self):

        sut = MenuProfile.RECORDER

        with self.assertRaises(NotImplementedError):
            _ = sut.get_event_map(InputDevice.HI3)

    def test_resolve_playback_hi1(self):

        expected: type = KeyboardEventMap

        sut = MenuProfile.PLAYBACK

        result = sut.get_event_map(InputDevice.HI1)

        self.assertEqual(expected, result)

    def test_resolve_playback_hi2(self):

        expected: type = StreamdeckEventMap

        sut = MenuProfile.PLAYBACK

        result = sut.get_event_map(InputDevice.HI2)

        self.assertEqual(expected, result)

    def test_resolve_playback_hi3(self):

        sut = MenuProfile.PLAYBACK

        with self.assertRaises(NotImplementedError):
            _ = sut.get_event_map(InputDevice.HI3)

    def test_instantiate_event_map(self):

        expected: type = StreamdeckEventMap

        sut = MenuProfile.DEFAULT

        result = sut.get_event_map(InputDevice.HI2)

        self.assertEqual(expected, result)

        instance: StreamdeckEventMap = cast(StreamdeckEventMap, result())

        values = instance.get_values()

        content = values["Main"]

        self.assertIsInstance(content, dict)
