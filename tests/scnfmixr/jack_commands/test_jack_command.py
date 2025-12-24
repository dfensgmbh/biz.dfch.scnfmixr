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

"""These tests should be in test_jack_command."""

import unittest

from biz.dfch.scnfmixr.jack_commands import AlsaToJack


class TestJackCommand(unittest.TestCase):
    """Tests for JackCommand."""

    def test_creating_alsa_to_jack_succeeds(self):
        """Creating an ALSA to JACK bridge succeeds."""

        expected = "Edgar"
        sut = AlsaToJack(expected, "null")

        self.assertIsNotNone(sut)

        result = sut.get_port_names()

        sut.stop()

        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].startswith(expected))
        self.assertTrue(result[0].endswith(":capture_0"))
        self.assertTrue(result[1].startswith(expected))
        self.assertTrue(result[1].endswith(":capture_1"))

    def test_creating_alsa_to_jack_with_connections_succeeds(self):
        """Creating an ALSA to JACK bridge and checking connections succeeds."""

        expected = "Edgar"
        sut = AlsaToJack(expected, "null")

        self.assertIsNotNone(sut)

        result = sut.get_ports()

        sut.stop()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, f"{expected}:capture_1")
        self.assertEqual(result[1].name, f"{expected}:capture_2")

        item = result[0]
        connections = item.get_connections()
        self.assertIsNotNone(connections)
        self.assertEqual(len(connections), 0)

        item = result[1]
        connections = item.get_connections()
        self.assertIsNotNone(connections)
        self.assertEqual(len(connections), 0)
