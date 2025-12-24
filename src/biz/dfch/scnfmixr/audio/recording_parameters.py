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

"""Recording parameters set by the user."""

from dataclasses import dataclass

from ..public.audio import FileFormat, Format, SampleRate


@dataclass
class RecordingParameters:
    """Recording parameters.

    Attributes:
        format (str): The format and codec of the recording.
        sampling_rate (int): The sampling rate of the recording.
        bit_depth (int): Bits per sample of the recording.
    """

    file_format: FileFormat = FileFormat.DEFAULT
    format: Format = Format.DEFAULT
    sampling_rate: int = SampleRate.DEFAULT
    skip_rc1: bool = False
    skip_rc2: bool = False
