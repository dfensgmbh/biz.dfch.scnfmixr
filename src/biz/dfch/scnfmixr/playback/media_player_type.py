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

"""Module media_player_type."""

from __future__ import annotations
from enum import StrEnum
import os


__all__ = [
    "MediaPlayerType",
]


class MediaPlayerType(StrEnum):
    """Supported media player types.

    Note: The defined socket names must match the defined socket names in 
    `.config/mpd/*/mpd.conf`.

    * PLAYBACK: `~/.config/mpd/playback/mpd.conf`
    * MENU: `~/.config/mpd/menu/mpd.conf`

    Base path is `/run/user/<uid>/` (for current user).

    Attributes:
        PLAYBACK: The player instance for audio playback.
        MENU: The player instance for menu audio feedback.
    """

    PLAYBACK = "mpd.playback.socket"
    MENU = "mpd.menu.socket"

    @staticmethod
    def get_value(key: MediaPlayerType) -> str:
        """Returns the value for the specified media player type."""

        assert isinstance(key, MediaPlayerType)

        if not hasattr(os, 'getuid'):
            raise EnvironmentError()

        uid = os.getuid()  # pylint: disable=E1101
        base_path = f"/run/user/{uid}"

        return f"{base_path}/{key.value}"
