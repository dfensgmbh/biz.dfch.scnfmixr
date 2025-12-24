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

"""Sound Devices MixPre-3 II"""  # noqa: E501 # pylint: disable=C0301

INFO = """\
Sound Devices, LLC MixPre-3 II at usb-xhci-hcd.0-2, high speed : USB Audio

Playback:
  Status: Running
    Interface = 1
    Altset = 2
    Packet Size = 432
    Momentary freq = 48002 Hz (0x6.0010)
    Feedback Format = 7.17
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 16
    Channel map: FL FR
    Sync Endpoint: 0x81 (1 IN)
    Sync EP Interface: 1
    Sync EP Altset: 1
    Implicit Feedback Mode: No
  Interface 1
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 24
    Channel map: FL FR
    Sync Endpoint: 0x81 (1 IN)
    Sync EP Interface: 1
    Sync EP Altset: 2
    Implicit Feedback Mode: No

Capture:
  Status: Running
    Interface = 2
    Altset = 2
    Packet Size = 432
    Momentary freq = 48000 Hz (0x6.0000)
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 16
    Channel map: FL FR
  Interface 2
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 24
    Channel map: FL FR
""".splitlines()  # noqa: E501 # pylint: disable=C0301
