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

"""Tests for module: `AudioPlayer`."""

from pathlib import Path
import time
import unittest

from biz.dfch.scnfmixr.ui.audio_player import AudioPlayer


class TestAudioPlayer(unittest.TestCase):
    """Tests for `AudioPlayer`."""

    def test_initialising_with_empty_name_throws(self):
        """Initialising with an empty jack name raises an error."""

        with self.assertRaises(AssertionError):
            _ = AudioPlayer("")

    def test_initialising_succeeds(self):
        """Initialising succeeds."""

        sut = AudioPlayer("arbitrary-name")

        self.assertIsNotNone(sut)

        sut.stop()

    def test_enqueuing_item_succeeds(self):
        """Enqueuing item succeeds."""

        path = Path(__file__).resolve().parent

        # Play in loop.
        item1: tuple[str, bool] = (str(path / "item-5s-1.flac"), True)
        # Play in loop.
        item2: tuple[str, bool] = (str(path / "item-5s-2.flac"), True)
        # Play in loop.
        item3: tuple[str, bool] = (str(path / "item-5s-3.flac"), True)

        sut = AudioPlayer("system")

        sut.enqueue(item1)
        sut.enqueue(item2)
        sut.enqueue(item3)

        time.sleep(2)

        # Skip to 2nd clip.
        sut.next()

        time.sleep(2)

        # Clear and stop queue.
        sut.stop()

        time.sleep(2)
