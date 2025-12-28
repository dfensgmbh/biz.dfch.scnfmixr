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

from __future__ import annotations

from .alsa_inferface_info import AlsaInterfaceInfo
from .audio_device import AudioDevice
from .audio_device_map import AudioDeviceMap
from .bit_depth import BitDepth
from .constant import Constant
from .file_format import FileFormat
from .format import Format
from .sample_rate import SampleRate


__all__ = [
    "AlsaInterfaceInfo",
    "AudioDevice",
    "AudioDeviceMap",
    "BitDepth",
    "Constant",
    "FileFormat",
    "Format",
    "SampleRate",
]
