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

"""Module audio_mixer."""

from __future__ import annotations
from abc import ABC

from ..system import (
    NotificationMedium,
)


__all__ = [
    "IAudioMixerMessage",
    "AudioMixer",
]


class IAudioMixerMessage(ABC):
    """Base type for all audio mixer messages."""


class AudioMixer:
    """AudioMixer messages."""

    class DefaultOutputChangedNotification(
            NotificationMedium, IAudioMixerMessage):
        """DefaultOutputChanged

        Args:
            value (str): The name of the new default output.
        """

        value: str

        def __init__(self, value: str):
            super().__init__()

            assert value and value.strip()

            self.value = value

    class StateChangedNotification(NotificationMedium, IAudioMixerMessage):
        """StateChanged"""

    class ConfigurationChangingNotification(
            NotificationMedium, IAudioMixerMessage):
        """ConfigurationChanging"""

    class ConfigurationChangedNotification(
            NotificationMedium, IAudioMixerMessage):
        """ConfigurationChanged"""

    class StartingNotification(NotificationMedium, IAudioMixerMessage):
        """Starting"""

    class StartedNotification(NotificationMedium, IAudioMixerMessage):
        """Started"""

    class StoppingNotification(NotificationMedium, IAudioMixerMessage):
        """Stopping"""

    class StoppedNotification(NotificationMedium, IAudioMixerMessage):
        """Stopped"""
