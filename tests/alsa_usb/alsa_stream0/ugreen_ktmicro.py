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

"""UGREEN KTMicro KT USB"""  # noqa: E501 # pylint: disable=C0301

INFO = """\
KTMicro KT USB Audio at usb-xhci-hcd.0-1.1, full speed : USB Audio

Playback:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ADAPTIVE)
    Rates: 44100, 48000, 96000
    Bits: 16
    Channel map: FL FR
  Interface 2
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ADAPTIVE)
    Rates: 44100, 48000, 96000
    Bits: 24
    Channel map: FL FR

Capture:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x81 (1 IN) (ASYNC)
    Rates: 44100, 48000
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501 # pylint: disable=C0301
