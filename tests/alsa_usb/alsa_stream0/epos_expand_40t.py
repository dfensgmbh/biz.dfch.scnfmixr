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

"""1395:0386 DSEA A/S EPOS EXPAND 40T

2 [E40T           ]: USB-Audio - EPOS EXPAND 40T
                     EPOS EPOS EXPAND 40T at usb-xhci-hcd.0-1, full speed
"""

INFO = """\
EPOS EPOS EXPAND 40T at usb-xhci-hcd.0-1, full speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x03 (3 OUT) (NONE)
    Rates: 48000
    Bits: 16
    Channel map: FL FR

Capture:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x83 (3 IN) (NONE)
    Rates: 16000
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501 # pylint: disable=C0301
