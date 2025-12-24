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

"""0b0e:0422 GN Netcom Jabra SPEAK 510 USB

 2 [USB            ]: USB-Audio - Jabra SPEAK 510 USB
                      Jabra SPEAK 510 USB at usb-xhci-hcd.0-1, full speed
"""

INFO = """\
Jabra SPEAK 510 USB at usb-xhci-hcd.0-1, full speed : USB Audio

Playback:
  Status: Running
    Interface = 1
    Altset = 1
    Packet Size = 192
    Momentary freq = 48000 Hz (0x30.0000)
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x03 (3 OUT) (NONE)
    Rates: 8000, 16000, 48000
    Bits: 16
    Channel map: FL FR

Capture:
  Status: Running
    Interface = 2
    Altset = 1
    Packet Size = 32
    Momentary freq = 16000 Hz (0x10.0000)
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x83 (3 IN) (NONE)
    Rates: 16000
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501 # pylint: disable=C0301
