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

"""Module format."""

from enum import StrEnum

from .bit_depth import BitDepth


class Format(StrEnum):
    """Audio encoding format."""

    S16_LE = "S16_LE"
    S24_LE = "S24_LE"
    S24_3LE = "S24_3LE"
    S32_LE = "S32_LE"
    F32_LE = "F32_LE"
    FLOAT_LE = "FLOAT_LE"
    DEFAULT = S24_3LE

    def get_bit_depth(self) -> int:
        """Returns the bit depth of a format."""

        match self:
            case Format.S16_LE:
                return BitDepth.B16
            case Format.S24_LE | Format.S24_3LE:
                return BitDepth.B24
            case Format.S32_LE | Format.F32_LE | Format.FLOAT_LE:
                return BitDepth.B32
            case _:
                raise LookupError
