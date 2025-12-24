# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""0582:0281 Roland Corp. SP-404MKII, 0582:02e7 Roland Corp. Roland SP-404MKII

Bus 003 Device 012: ID 0582:0281 Roland Corp. SP-404MKII
Bus 003 Device 013: ID 0582:02e7 Roland Corp. Roland SP-404MKII


 5 [SP404MKII      ]: USB-Audio - SP-404MKII
                      Roland SP-404MKII at usb-xhci-hcd.1-1.4.2, full speed
"""

INFO = """\
Roland SP-404MKII at usb-xhci-hcd.1-1.4.2, full speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 4
    Endpoint: 0x0d (13 OUT) (ADAPTIVE)
    Rates: 48000
    Bits: 16
    Channel map: FL FR RL RR

Capture:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x8e (14 IN) (ASYNC)
    Rates: 48000
    Bits: 16
    Channel map: FL FR
""".splitlines()  # noqa: E501 # pylint: disable=C0301
