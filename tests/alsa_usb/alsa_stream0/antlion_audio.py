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

"""0d8c:002c C-Media Electronics, Inc. Antlion USB adapter

 2 [adapter        ]: USB-Audio - Antlion USB adapter
                      Antlion Audio Antlion USB adapter at usb-xhci-hcd.1-1.2, full speed
"""  # noqa: E501 # pylint: disable=C0301

INFO = """\
Antlion Audio Antlion USB adapter at usb-xhci-hcd.1-1.2, full speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ADAPTIVE)
    Rates: 48000, 44100
    Bits: 16
    Channel map: FL FR

Capture:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x82 (2 IN) (ADAPTIVE)
    Rates: 48000, 44100
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501 # pylint: disable=C0301
