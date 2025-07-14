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
