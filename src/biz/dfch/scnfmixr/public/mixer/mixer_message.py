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

"""Module mixer_message."""

from __future__ import annotations
from abc import ABC

from ..system import (
    NotificationMedium,
    CommandMedium,
)

__all__ = [
    "MixerMessage",
    "IAudioMixerMessage",
    "IAudioRecorderMessage",
]


class IAudioMixerMessage(ABC):
    """Base type for all audio mixer messages."""


class IAudioRecorderMessage(ABC):
    """Base type for all audio recorder messages."""


class MixerMessage:
    """Mixer messages."""

    class Recorder:
        """AudioRecorder messages."""

        class StateErrorMessage(NotificationMedium, IAudioRecorderMessage):
            """State Error."""

        class ConfigurationChanging(NotificationMedium, IAudioRecorderMessage):
            """Configuration Changing."""

        class ConfigurationChanged(NotificationMedium, IAudioRecorderMessage):
            """Configuration Changed."""

        class StartingMessage(NotificationMedium, IAudioRecorderMessage):
            """Status Starting."""

        class StartedMessage(NotificationMedium, IAudioRecorderMessage):
            """Status Started."""

        class StoppingMessage(NotificationMedium, IAudioRecorderMessage):
            """Status Stopping."""

        class StoppedMessage(NotificationMedium, IAudioRecorderMessage):
            """Status Stopped."""

        class RecordingStopCommand(CommandMedium, IAudioRecorderMessage):
            """Stop recording."""

        class RecordingStartCommand(CommandMedium, IAudioRecorderMessage):
            """Start recording."""

            items: list[str]

            def __init__(self, items: list[str]):
                super().__init__()

                assert items and isinstance(items, list)

                self.items = items

        class RecordingPauseCommand(CommandMedium, IAudioRecorderMessage):
            """Pause recording."""

        class RecordingResumeCommand(CommandMedium, IAudioRecorderMessage):
            """Resume recording."""

    class Mixer:
        """AudioMixer messages."""

        class DefaultOutputChanged(NotificationMedium, IAudioMixerMessage):
            """DefaultOutputChanged

            Args:
                value (str): The name of the new default output.
            """

            value: str

            def __init__(self, value: str):
                super().__init__()

                assert value and value.strip()

                self.value = value

        class StateChanged(NotificationMedium, IAudioMixerMessage):
            """StateChanged"""

        class ConfigurationChanging(NotificationMedium, IAudioMixerMessage):
            """ConfigurationChanging"""

        class ConfigurationChanged(NotificationMedium, IAudioMixerMessage):
            """ConfigurationChanged"""

        class Starting(NotificationMedium, IAudioMixerMessage):
            """Starting"""

        class Started(NotificationMedium, IAudioMixerMessage):
            """Started"""

        class Stopping(NotificationMedium, IAudioMixerMessage):
            """Stopping"""

        class Stopped(NotificationMedium, IAudioMixerMessage):
            """Stopped"""
