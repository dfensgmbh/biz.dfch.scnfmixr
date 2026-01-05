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

"""Module audio_recorder."""

from __future__ import annotations
from abc import ABC
import time

from ..storage import FileName
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

    class RecordingCuePointCommand(CommandMedium, IAudioRecorderMessage):
        """Request for creating a cue marker."""

        value: float

        def __init__(self, value: float = time.monotonic()):
            super().__init__()

            assert isinstance(value, float)

            self.value = value

    class DeleteLastRecordingNotification(NotificationMedium,
                                          IAudioRecorderMessage):
        """Notification result of the DeleteLastRecording command."""

        value: bool

        def __init__(self, value: bool):
            super().__init__()

            assert isinstance(value, bool)

            self.value = value

    class DeleteLastRecordingCommand(CommandMedium, IAudioRecorderMessage):
        """Delete the last recording."""

    class RecordingStopCommand(CommandMedium, IAudioRecorderMessage):
        """Stop recording."""

    class RecordingStartCommand(CommandMedium, IAudioRecorderMessage):
        """Start recording."""

        items: dict[str, list[FileName]]

        def __init__(self, items: dict[str, list[FileName]]):
            super().__init__()

            assert items and isinstance(items, dict)
            assert all(isinstance(e, str) for e in items)
            assert all(
                isinstance(e, list) and all(
                    isinstance(item, FileName)
                    for item in e) for e in items.values())

            self.items = items

    class RecordingPauseCommand(CommandMedium, IAudioRecorderMessage):
        """Pause recording."""

    class RecordingResumeCommand(CommandMedium, IAudioRecorderMessage):
        """Resume recording."""
