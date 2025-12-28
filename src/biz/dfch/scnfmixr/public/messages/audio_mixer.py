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
