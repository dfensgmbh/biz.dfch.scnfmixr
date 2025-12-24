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

"""Logical names of mixbus devices in the system."""

from enum import IntEnum, StrEnum

from .connection import Connection

__all__ = [
    "MixbusDevice",
    "IsoChannelDry",
    "IsoChannelWet",
]


class MixbusDevice(StrEnum):
    """Logical names of mixbus devices in the system.

    Attributes:
        MX0: The master stereo bus.
        MX1: The isolated DRY track bus (includes master left and right).
        MX2: The isolated WET track bus (includes master left and right).
        MX3: The LCL stereo bus.
        MX4: The EX1 stereo bus.
        MX5: The EX2 stereo bus.
        MX6: The monitoring stereo bus.
        DR0: The 1st dry stereo channel strip.
        WT0: The 1st wet stereo channel strip.
        DR1: The 2nd dry stereo channel strip.
        WT1: The 2nd wet stereo channel strip.
        DR2: The 3rd dry stereo channel strip.
        WT2: The 3rd wet stereo channel strip.
    """

    MX0 = Connection.jack_mixbus_client_from_base("MX0")
    MX1 = Connection.jack_mixbus_client_from_base("MX1")
    MX2 = Connection.jack_mixbus_client_from_base("MX2")
    MX3 = Connection.jack_mixbus_client_from_base("MX3")
    MX4 = Connection.jack_mixbus_client_from_base("MX4")
    MX5 = Connection.jack_mixbus_client_from_base("MX5")
    MX6 = Connection.jack_mixbus_client_from_base("MX6")
    DR0 = Connection.jack_mixbus_client_from_base("DR0")
    WT0 = Connection.jack_mixbus_client_from_base("WT0")
    DR1 = Connection.jack_mixbus_client_from_base("DR1")
    WT1 = Connection.jack_mixbus_client_from_base("WT1")
    DR2 = Connection.jack_mixbus_client_from_base("DR2")
    WT2 = Connection.jack_mixbus_client_from_base("WT2")


class IsoChannelDry(IntEnum):
    """Iso channel DRY names."""

    MST_LEFT = 0
    MST_RIGHT = 1
    DR0_LEFT = 2
    DR0_RIGHT = 3
    DR1_LEFT = 4
    DR1_RIGHT = 5
    DR2_LEFT = 6
    DR2_RIGHT = 7


class IsoChannelWet(IntEnum):
    """Iso channel WET names."""

    MST_LEFT = 0
    MST_RIGHT = 1
    WT0_LEFT = 2
    WT0_RIGHT = 3
    WT1_LEFT = 4
    WT1_RIGHT = 5
    WT2_LEFT = 6
    WT2_RIGHT = 7
