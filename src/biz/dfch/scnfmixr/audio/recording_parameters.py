# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Recording parameters set by the user."""

from dataclasses import dataclass, field

from ..public.audio import FileFormat
from ..public.audio import Format
from ..public.audio import SampleRate
from ..public.mixer import MixbusDevice


@dataclass
class RecordingParameters:
    """Recording parameters.

    Attributes:
        format (str): The format and codec of the recording.
        sampling_rate (int): The sampling rate of the recording.
        bit_depth (int): Bits per sample of the recording.
        targets (list[MixbusDevice]): The mixbus devices to record.
    """

    file_format: FileFormat = FileFormat.DEFAULT
    format: Format = Format.DEFAULT
    sampling_rate: int = SampleRate.DEFAULT
    targets: list[MixbusDevice] = field(default_factory=list)
