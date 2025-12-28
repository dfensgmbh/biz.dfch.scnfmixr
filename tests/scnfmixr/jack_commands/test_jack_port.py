# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""Testing JACK ports. Platform dependent. Requires a running JACK server."""

import unittest

from biz.dfch.scnfmixr.jack_commands import JackPort


class TestJackPort(unittest.TestCase):
    """Testing JackConnection"""

    def test_known_port_returns_true(self) -> None:
        """Testing with an known port returns true."""

        sut = JackPort("system:playback_1")

        result = sut.exists

        self.assertTrue(result)

    def test_unknown_port_returns_false(self) -> None:
        """Testing with an unknown port returns false."""

        sut = JackPort("arbitrary-name:arbitrary-suffix_1")

        result = sut.exists

        self.assertFalse(result)

    def test_connectsto_and_disconnectall_succeeds(self) -> None:
        """Connecting to a port and disconnecting from it succeeds."""

        sut = JackPort("system:capture_1")

        result = sut.connect_to("system:playback_1")

        self.assertTrue(result)

        result = sut.disconnect_all()
        self.assertTrue(result)

    def test_connectsto_unknown_port_fails(self) -> None:
        """Connecting to an unknown port fails."""

        sut = JackPort("system:capture_1")

        result = sut.connect_to("unknown-client:unknown_port_667")

        self.assertFalse(result)

    def test_get_ports_succeeds(self) -> None:
        """Enumerating all ports succeeds."""

        result = JackPort.get_ports()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertLess(0, len(result))

        self.assertTrue(any("system:" in item.name for item in result))
        self.assertTrue(any(":capture_" in item.name for item in result))
        self.assertTrue(any(":playback_" in item.name for item in result))

    def test_get_single_port_succeeds(self) -> None:
        """Enumerating existing port succeeds."""

        result = JackPort.get_ports("system:capture_1")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))

        self.assertTrue(any("system:" in item.name for item in result))
        self.assertTrue(any(":capture_" in item.name for item in result))
