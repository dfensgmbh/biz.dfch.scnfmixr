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
