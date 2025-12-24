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

"""Module test_jack_command2."""

from __future__ import annotations
import unittest
from unittest.mock import patch

from biz.dfch.scnfmixr.jack_commands import JackConnection
from .mock_process import (
    MockProcessJackConnectSucceeds,
    MockProcessJackConnectFails,
    MockProcessJackDisconnectFails,
    MockProcessGetConnections2,
    MockProcessGetConnections3,
)


class TestJackConnection2(unittest.TestCase):
    """TestJackCommand2"""

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackConnectSucceeds)
    def test_factory_create_succeeds(self):
        """test_Sth"""

        source = "Alsa:LCL-I:capture_1"
        sink = "Alsa:LCL-O:playback_1"

        sut = JackConnection.Factory.create(source, sink)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_connected)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackConnectFails)
    def test_factory_create_fails(self):
        """Connecting an existing connection fails."""

        source = "Alsa:LCL-I:capture_1"
        sink = "Alsa:LCL-O:playback_1"

        sut = JackConnection.Factory.create(source, sink)
        self.assertIsNone(sut)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackConnectSucceeds)
    def test_disconnect_succeds(self):
        """Disconnecting a session succeeds."""

        source = "Alsa:LCL-I:capture_1"
        sink = "Alsa:LCL-O:playback_1"

        sut = JackConnection.Factory.create(source, sink)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_connected)

        result = sut.disconnect()
        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackDisconnectFails)
    def test_disconnect_fails(self):
        """Disconnecting a connecting fails."""

        source = "Alsa:LCL-I:capture_1"
        sink = "Alsa:LCL-O:playback_1"

        sut = JackConnection.Factory.create(source, sink)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_connected)

        result = sut.disconnect()
        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackDisconnectFails)
    def test_check_connection_returns_true(self):
        """Checking a non-existing connection succeds."""
        self.skipTest("Not yet implemented.")

        source = "Alsa:LCL-I:capture_1"
        sink = "existing_sink"

        result = JackConnection.check_connection(source, sink)

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessJackDisconnectFails)
    def test_check_connection_returns_false(self):
        """Checking a non-existing connection fails."""
        self.skipTest("Not yet implemented.")

        source = "Alsa:LCL-I:capture_1"
        sink = "non_existing_sink"

        result = JackConnection.check_connection(source, sink)

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections2)
    def test_get_connections_for_name_succeeds(self):
        """Retrieving connections for a given name succeeds."""

        source = "Alsa:LCL-I:capture_1"
        # See MockVisitorContainsConnection for actual connections.
        expected = "Alsa:LCL-O:playback_1"

        result = JackConnection.get_connections2()
        self.assertTrue(source in result)
        self.assertTrue(expected in result[source])

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections2)
    def test_get_connections_for_name_fails(self):
        """Retrieving connections for a given name fails."""

        source = "Alsa:LCL-I:capture_1"
        # See MockVisitorContainsConnection for actual connections.
        expected = "Alsa:EX2-O:playback_2"

        result = JackConnection.get_connections2()
        self.assertTrue(source in result)
        self.assertFalse(expected in result[source], result[source])

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections2)
    def test_get_connections2_succeeds(self):
        """Retrieving connections in a structured form."""

        # See MockProcessGetConnections2 for actual connections.

        result = JackConnection.get_connections2()

        self.assertEqual(16, len(result), result)

        key = 'system:capture_1'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'system:capture_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'system:playback_1'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'system:playback_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:LCL-I:capture_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX1-I:capture_1'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX1-I:capture_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX2-I:capture_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX2-I:capture_1'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX2-O:playback_1'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:EX2-O:playback_2'
        self.assertTrue(key in result)
        self.assertEqual(0, len(result[key]), (key, result[key]))

        key = 'Alsa:LCL-O:playback_1'
        self.assertTrue(key in result)
        self.assertEqual(1, len(result[key]), (key, result[key]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[key], (value, result[key]))

        key = 'Alsa:LCL-O:playback_2'
        self.assertTrue(key in result)
        self.assertEqual(1, len(result[key]), (key, result[key]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[key], (value, result[key]))

        key = 'Alsa:EX1-O:playback_2'
        self.assertTrue(key in result)
        self.assertEqual(1, len(result[key]), (key, result[key]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[key], (value, result[key]))

        key = 'Alsa:LCL-I:capture_1'
        self.assertTrue(key in result)
        self.assertEqual(4, len(result[key]), (key, result[key]))
        value = 'Alsa:LCL-O:playback_1'
        self.assertTrue(value in result[key], (value, result[key]))
        value = 'Alsa:LCL-O:playback_2'
        self.assertTrue(value in result[key], (value, result[key]))
        value = 'Alsa:EX1-O:playback_1'
        self.assertTrue(value in result[key], (value, result[key]))
        value = 'Alsa:EX1-O:playback_2'
        self.assertTrue(value in result[key], (value, result[key]))

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_connections3_succeeds(self):
        """Retrieving connections in a structured form."""

        # See MockProcessGetConnections3 for actual connections.

        result = JackConnection.get_connections3()

        self.assertEqual(16, len(result), result)

        key = 'system:capture_1'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'system:capture_2'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'system:playback_1'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'system:playback_2'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:LCL-I:capture_2'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX1-I:capture_1'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX1-I:capture_2'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX2-I:capture_2'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX2-I:capture_1'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX2-O:playback_1'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:EX2-O:playback_2'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            0, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))

        key = 'Alsa:LCL-O:playback_1'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            1, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))

        key = 'Alsa:LCL-O:playback_2'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            1, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))

        key = 'Alsa:EX1-O:playback_2'
        is_sink = True
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            1, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))
        value = 'Alsa:LCL-I:capture_1'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))

        key = 'Alsa:LCL-I:capture_1'
        is_sink = False
        self.assertTrue(
            any(e == key and f == is_sink
                for e, f in result.keys()))  # pylint: disable=C0201
        self.assertEqual(
            4, len(result[(key, is_sink)]), (key, result[(key, is_sink)]))
        value = 'Alsa:LCL-O:playback_1'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))
        value = 'Alsa:LCL-O:playback_2'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))
        value = 'Alsa:EX1-O:playback_1'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))
        value = 'Alsa:EX1-O:playback_2'
        self.assertTrue(value in result[(key, is_sink)],
                        (value, result[(key, is_sink)]))
