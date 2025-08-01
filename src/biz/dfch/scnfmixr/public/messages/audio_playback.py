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

        value: int

        def __init__(self, value: int = -10):
            assert isinstance(value, int) and 0 > value

            super().__init__(value)

            self.value = value

    class SeekNextCommand(SeekRelativeCommand, IAudioPlaybackMessage):
        """SeekNextCommand"""

        value: int

        def __init__(self, value: int = 10):
            assert isinstance(value, int) and 0 < value

            super().__init__(value)

            self.value = value
