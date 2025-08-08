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
