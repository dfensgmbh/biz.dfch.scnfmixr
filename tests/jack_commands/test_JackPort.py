# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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
