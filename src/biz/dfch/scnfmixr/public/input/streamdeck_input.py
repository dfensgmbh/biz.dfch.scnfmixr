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

from enum import IntEnum

__all__ = [
    "StreamdeckInput",
]


class StreamdeckInput(IntEnum):
    """
    Defines Elgato Streamdeck key numbers.
    """

    # Elgato Streamdeck MK.2
    # Row 1.
    KEY_00 = 0x00
    KEY_01 = 0x01
    KEY_02 = 0x02
    KEY_03 = 0x03
    KEY_04 = 0x04

    # Row 2.
    KEY_05 = 0x05
    KEY_06 = 0x06
    KEY_07 = 0x07
    KEY_08 = 0x08
    KEY_09 = 0x09

    # Row 3.
    KEY_0A = 0x0A
    KEY_0B = 0x0B
    KEY_0C = 0x0C
    KEY_0D = 0x0D
    KEY_0E = 0x0E

    KEY_0F = 0x0F
