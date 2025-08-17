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

"""Tests for module: test_state_machine."""

from __future__ import annotations
import unittest
from unittest.mock import patch
from enum import StrEnum

from biz.dfch.scnfmixr.core import StateMachine


class MediaPlayerTypeMock(StrEnum):
    """MediaPlayerTypeMock"""

    PLAYBACK = "mpd.playback.socket"
    MENU = "mpd.menu.socket"

    @staticmethod
    def get_value(key: MediaPlayerTypeMock) -> str:
        """Returns a mocked value."""
        return f"/run/usr/1000/{key.value}"


class TestStateMachine(unittest.TestCase):
    """TestStateMachine"""

    @patch('biz.dfch.scnfmixr.playback.audio_menu.MediaPlayerType',
           new=MediaPlayerTypeMock)
    @patch('biz.dfch.scnfmixr.playback.media_player_client.MediaPlayerType',
           new=MediaPlayerTypeMock)
    def test_if_state_machine_is_valid(self):
        """Tests if the state machine is valid and does not throw any
        execptions during initialise."""

        sut = StateMachine()

        sut.initialise()
