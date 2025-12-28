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

"""Tests for module: `AudioPlayer`."""

from pathlib import Path
import time
import unittest

from ui.output.AudioPlayer import AudioPlayer


class TestAudioPlayer(unittest.TestCase):
    """Tests for `AudioPlayer`."""

    def test_enqueuing_item_succeeds(self):
        """Enqueuing and skipping files. Clearing and stopping queue."""

        # We use audio files in the same folder as the test is. These files are
        # of a specific length (5s), so we can time accordingly.
        path = Path(__file__).resolve().parent

        # Play in loop.
        item1: tuple[str, bool] = (str(path / "item-5s-1.flac"), True)
        # Play in loop.
        item2: tuple[str, bool] = (str(path / "item-5s-2.flac"), True)
        # Play in loop.
        item3: tuple[str, bool] = (str(path / "item-5s-3.flac"), True)

        # Connect to "system" sink. If this sink does not exist in this test,
        # the player will not be able to connect but play anyway. You can check
        # with `jack_lsp`.
        sut = AudioPlayer("system")

        sut.enqueue(item1)
        sut.enqueue(item2)
        sut.enqueue(item3)

        time.sleep(5 + 5 + 5)

        sut.next()

        time.sleep(5)

        sut.clear()
        sut.stop()
