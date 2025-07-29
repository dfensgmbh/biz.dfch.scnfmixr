# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Logical names of mixbus devices in the system."""

from enum import IntEnum, StrEnum, auto

from .connection import Connection


class MixbusDevice(StrEnum):
    """Logical names of mixbus devices in the system.

    Attributes:
        MX0: The master stereo bus.
        MX1: The isolated track bus (includes master left and right).
        MX2: The monitoring stereo bus.
        MX3: The LCL stereo bus.
        MX4: The EX1 stereo bus.
        MX5: The EX2 stereo bus.
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
    DR0 = Connection.jack_mixbus_client_from_base("DR0")
    WT0 = Connection.jack_mixbus_client_from_base("WT0")
    DR1 = Connection.jack_mixbus_client_from_base("DR1")
    WT1 = Connection.jack_mixbus_client_from_base("WT1")
    DR2 = Connection.jack_mixbus_client_from_base("DR2")
    WT2 = Connection.jack_mixbus_client_from_base("WT2")


class IsoChannel(IntEnum):
    """Iso channel names."""

    LEFT = 0
    RIGHT = 1
    DR0_LEFT = 2
    DR0_RIGHT = 3
    DR1_LEFT = 4
    DR1_RIGHT = 5
    DR2_LEFT = 6
    DR2_RIGHT = 7
    WT0_LEFT = 8
    WT0_RIGHT = 9
    WT1_LEFT = 10
    WT1_RIGHT = 11
    WT2_LEFT = 12
    WT2_RIGHT = 13
