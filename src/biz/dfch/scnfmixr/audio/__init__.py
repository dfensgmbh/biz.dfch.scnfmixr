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

"""Package audio."""

from .Asound import Asound
from .asound_card_info import AsoundCardInfo
from .proc_alsa_usb_device_info import ProcAlsaUsbDeviceInfo
from .recording_parameters import RecordingParameters
from .audio_device_info import AudioDeviceInfo
from .usb_audio_device_not_detected_error import UsbAudioDeviceNotDetectedError
from .Usb import Usb

__all__ = [
    "Asound",
    "AsoundCardInfo",
    "ProcAlsaUsbDeviceInfo",
    "RecordingParameters",
    "AudioDeviceInfo",
    "UsbAudioDeviceNotDetectedError",
    "Usb",
]
