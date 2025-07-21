# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module test_connection_info."""

import unittest
from unittest.mock import patch

from biz.dfch.scnfmixr.jack_commands.jack_connection import JackConnection
from biz.dfch.scnfmixr.jack_commands.connection_info import ConnectionInfo
from .mock_process import MockProcessGetConnections3


class TestConnectionInfo(unittest.TestCase):
    """TestConnectionInfo"""

    def test_from_entry_succeeds(self):
        """Entry can be correctly split into client and port."""

        client1_exp = "Alsa:LCL-O"
        port1_exp = "capture_1"
        client1, port1 = ConnectionInfo.from_entry(f"{client1_exp}:{port1_exp}")
        self.assertEqual(client1_exp, client1)
        self.assertEqual(port1_exp, port1)

    def test_tp_entry_succeeds(self):
        """Entry can be correctly created from client and port."""

        client1_exp = "Alsa:LCL-O"
        port1_exp = "capture_1"
        result = ConnectionInfo.to_entry(client1_exp, port1_exp)
        self.assertEqual(f"{client1_exp}:{port1_exp}", result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_all_succeeds(self):
        """All connections are returned correctly."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.all

        self.assertEqual(4, len(result), result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_clients_succeeds(self):
        """Clients returned connections grouped by client name."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.clients

        self.assertEqual(3, len(result), result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_client_true(self):
        """Client exists and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_client("Alsa:LCL-O")

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_client_false(self):
        """Client does not exist and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_client("arbitrary-non-existing-client")

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_entry_true(self):
        """Entry exists and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_entry("Alsa:LCL-I:capture_1")

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_entry_false(self):
        """Entry does not exist and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_entry("arbitrary-non-existing-client:capture_1")

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_source_true(self):
        """Entry is source and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_source("Alsa:LCL-I:capture_1")

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_source_false(self):
        """Entry is not source and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_source("Alsa:LCL-O:playback_1")

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_sink_true(self):
        """Entry is sink and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_sink("Alsa:LCL-O:playback_1")

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_sink_false(self):
        """Entry is not sink and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_sink("Alsa:LCL-I:capture_1")

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_sources(self):
        """Returns sources."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.sources

        self.assertEqual(8, len(result), result)
        self.assertTrue('system:capture_1' in result)
        self.assertTrue('system:capture_2' in result)
        self.assertTrue('Alsa:LCL-I:capture_1' in result)
        self.assertTrue('Alsa:LCL-I:capture_2' in result)
        self.assertTrue('Alsa:EX1-I:capture_1' in result)
        self.assertTrue('Alsa:EX1-I:capture_2' in result)
        self.assertTrue('Alsa:EX2-I:capture_1' in result)
        self.assertTrue('Alsa:EX2-I:capture_2' in result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_sinks(self):
        """Returns sinks."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.sinks

        self.assertEqual(8, len(result), result)
        self.assertTrue('system:playback_1' in result)
        self.assertTrue('system:playback_2' in result)
        self.assertTrue('Alsa:LCL-O:playback_1' in result)
        self.assertTrue('Alsa:LCL-O:playback_2' in result)
        self.assertTrue('Alsa:EX1-O:playback_1' in result)
        self.assertTrue('Alsa:EX1-O:playback_2' in result)
        self.assertTrue('Alsa:EX2-O:playback_1' in result)
        self.assertTrue('Alsa:EX2-O:playback_2' in result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_has_connection_true(self):
        """Client has connections and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.has_connections("Alsa:LCL-I")

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_has_connections_false(self):
        """Client has connections and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.has_connections("system")

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_connections_succeeds(self):
        """Client has connections and returns list."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.get_connections("Alsa:LCL-I")

        self.assertEqual(4, len(result))

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_connections2_succeeds(self):
        """Client has connections and returns list."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.get_connections("Alsa:LCL-O")

        self.assertEqual(2, len(result))

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_connections_fails(self):
        """Client has connections and returns empty."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.get_connections("system")

        self.assertEqual(0, len(result))

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_connected_to_true(self):
        """Entry is connected and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_connected_to(
            "Alsa:LCL-I:capture_1",
            "Alsa:EX1-O:playback_1",
        )

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_connected_to_false(self):
        """Entry is not connected and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_connected_to(
            "Alsa:LCL-I:capture_1",
            "Alsa:EX2-O:playback_1",
        )

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_connected_true(self):
        """Entry is connected and returns true."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_connected(
            "Alsa:LCL-I:capture_1",
        )

        self.assertTrue(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_is_connected_false(self):
        """Entry is not connected and returns false."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.is_connected(
            "Alsa:EX2-O:playback_1",
        )

        self.assertFalse(result)

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_ports_succeeds(self):
        """Returns ports for client name."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.get_ports("Alsa:LCL-O")

        self.assertEqual(2, len(result), result)
        self.assertEqual("playback_1", result[0])
        self.assertEqual("playback_2", result[1])

    @patch("biz.dfch.scnfmixr.jack_commands.jack_connection.Process",
           new=MockProcessGetConnections3)
    def test_get_entries_succeeds(self):
        """Returns ports for client name."""

        conn = JackConnection.get_connections3()

        sut = ConnectionInfo(conn)

        result = sut.get_entries("Alsa:LCL-O")

        self.assertEqual(2, len(result), result)
        self.assertEqual("Alsa:LCL-O:playback_1", result[0])
        self.assertEqual("Alsa:LCL-O:playback_2", result[1])
