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

"""Module audio_recorder."""

from __future__ import annotations
from abc import ABC

from ..system import (
    NotificationHigh,
    NotificationMedium,
    CommandMedium,
)


__all__ = [
    "IAudioRecorderMessage",
    "AudioRecorder",
]


class IAudioRecorderMessage(ABC):
    """Base type for all audio recorder messages."""


class AudioRecorder:
    """AudioRecorder messages."""

    class StateErrorMessage(NotificationMedium, IAudioRecorderMessage):
        """State Error."""

    class ConfigurationChangingNotification(
            NotificationMedium, IAudioRecorderMessage):
        """Configuration Changing."""

    class RecordingCrashedNotification(
            NotificationHigh, IAudioRecorderMessage):
        """RecordingCrashed."""

    class ConfigurationChangedNotification(
            NotificationMedium, IAudioRecorderMessage):
        """Configuration Changed."""

    class StartingNotification(NotificationMedium, IAudioRecorderMessage):
        """Status Starting."""

    class StartedNotification(NotificationMedium, IAudioRecorderMessage):
        """Status Started."""

    class StoppingNotification(NotificationMedium, IAudioRecorderMessage):
        """Status Stopping."""

    class StoppedNotification(NotificationMedium, IAudioRecorderMessage):
        """Status Stopped."""

    class RecordingStopCommand(CommandMedium, IAudioRecorderMessage):
        """Stop recording."""

    class RecordingStartCommand(CommandMedium, IAudioRecorderMessage):
        """Start recording."""

        items: list[str]
        jack_device: str

        def __init__(self, items: list[str], jack_device: str):
            super().__init__()

            assert items and isinstance(items, list)
            assert isinstance(jack_device, str) and jack_device.strip()

            self.items = items
            self.jack_device = jack_device

    class RecordingPauseCommand(CommandMedium, IAudioRecorderMessage):
        """Pause recording."""

    class RecordingResumeCommand(CommandMedium, IAudioRecorderMessage):
        """Resume recording."""
