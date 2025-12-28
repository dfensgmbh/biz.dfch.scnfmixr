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

"""Module message_priority."""

from enum import IntEnum


__all__ = [
    "MessagePriority",
]


class MessagePriority(IntEnum):
    """Defines the different priorities for queue items."""

    DEFAULT = 128

    MEDIUM = DEFAULT
    LEVEL_80 = MEDIUM

    HIGHEST = 255
    LEVEL_FF = HIGHEST

    HIGH = 192
    LEVEL_C0 = HIGH

    LOW = 64
    LEVEL_40 = LOW

    LOWEST = 0
    LEVEL_00 = LOWEST
