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

"""Module sample_rate."""

from enum import IntEnum


class SampleRate(IntEnum):
    """Supported sample rates."""

    R08000 = 8000
    R16000 = 16000
    R24000 = 24000
    R32000 = 32000
    R44100 = 44100
    CD = R44100
    R48000 = 48000
    R88200 = 88200
    R96000 = 96000
    SACD = R96000
    DEFAULT = 48000
