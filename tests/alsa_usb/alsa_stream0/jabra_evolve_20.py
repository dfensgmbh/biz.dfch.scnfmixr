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

"""0b0e:0302 GN Netcom Jabra EVOLVE 20 SE MS

2 [MS             ]: USB-Audio - Jabra EVOLVE 20 SE MS
                     GN Netcom A/S Jabra EVOLVE 20 SE MS at usb-xhci-hcd.0-1, full speed
"""  # noqa: E501 # pylint: disable=C0301

INFO = """\
GN Netcom A/S Jabra EVOLVE 20 SE MS at usb-xhci-hcd.0-1, full speed : USB Audio

Playback:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x04 (4 OUT) (SYNC)
    Rates: 8000, 16000, 32000, 44100, 48000
    Bits: 16
    Channel map: MONO

Capture:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x83 (3 IN) (SYNC)
    Rates: 8000, 16000, 44100, 48000
    Bits: 16
    Channel map: MONO
""".splitlines()
