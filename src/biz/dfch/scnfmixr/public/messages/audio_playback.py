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

"""Module audio_playback."""

from __future__ import annotations

from ..system import (
    # NotificationMedium,
    CommandMedium,
    MessageBase,
)


__all__ = [
    "IAudioPlaybackMessage",
    "AudioPlayback",
]


class IAudioPlaybackMessage(MessageBase):
    """Base type for all audio mixer messages."""


class AudioPlayback:
    """AudioPlayback messages."""

    class PlaybackStartCommand(CommandMedium, IAudioPlaybackMessage):
        """PlaybackStopCommand"""

    class PlaybackStopCommand(CommandMedium, IAudioPlaybackMessage):
        """PlaybackStopCommand"""

    class PauseResumeCommand(CommandMedium, IAudioPlaybackMessage):
        """PauseResumeNotification"""

    class ClipStartCommand(CommandMedium, IAudioPlaybackMessage):
        """ClipStartCommand"""

    class ClipEndCommand(CommandMedium, IAudioPlaybackMessage):
        """ClipEndCommand"""

    class ClipPreviousCommand(CommandMedium, IAudioPlaybackMessage):
        """ClipPreviousCommand"""

    class ClipNextCommand(CommandMedium, IAudioPlaybackMessage):
        """ClipNextCommand"""

    class CuePointPreviousCommand(CommandMedium, IAudioPlaybackMessage):
        """CuePointPreviousCommand"""

    class CuePointNextCommand(CommandMedium, IAudioPlaybackMessage):
        """CuePointNextCommand"""

    class SeekAbsoluteCommand(CommandMedium, IAudioPlaybackMessage):
        """SeekAbsoluteCommand"""

        value: int

        def __init__(self, value: int):
            super().__init__()

            assert isinstance(value, int) and 0 <= value

            self.value = value

    class SeekRelativeCommand(CommandMedium, IAudioPlaybackMessage):
        """SeekRelativeCommand"""

        value: int

        def __init__(self, value: int):
            super().__init__()

            assert isinstance(value, int) and 0 != value

            self.value = value

    class SeekPreviousCommand(SeekRelativeCommand, IAudioPlaybackMessage):
        """SeekPreviousCommand"""

        SEEK_VALUE: int = -10

        value: int

        def __init__(self, value: int = SEEK_VALUE):
            assert isinstance(value, int) and 0 > value

            super().__init__(value)

            self.value = value

    class SeekNextCommand(SeekRelativeCommand, IAudioPlaybackMessage):
        """SeekNextCommand"""

        SEEK_VALUE: int = 30

        value: int

        def __init__(self, value: int = SEEK_VALUE):
            assert isinstance(value, int) and 0 < value

            super().__init__(value)

            self.value = value
