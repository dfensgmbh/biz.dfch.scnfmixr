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

"""0b0e:24f1 GN Netcom Jabra Speak2 75

 4 [J75            ]: USB-Audio - Jabra Speak2 75
                      Jabra Speak2 75 at usb-xhci-hcd.0-1.1, full speed
"""

INFO = """\
Jabra Speak2 75 at usb-xhci-hcd.0-1.1, full speed : USB Audio

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
    Rates: 8000, 16000, 32000, 44100, 48000
    Bits: 16
    Channel map: FL FR

Capture:
  Status: Running
    Interface = 2
    Altset = 1
    Packet Size = 64
    Momentary freq = 32000 Hz (0x20.0000)
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x83 (3 IN) (NONE)
    Rates: 32000
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501 # pylint: disable=C0301
