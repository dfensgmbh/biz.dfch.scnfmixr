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

"""Mock object for AlsaStreamInfoParser."""


from biz.dfch.scnfmixr.alsa_usb import AlsaStreamInfoParser


class MockAlsaStreamInfoParser(AlsaStreamInfoParser):
    """Mock AlsaStreamInfoParser."""

    _CARD2_STREAM_INFO = """\
Jabra SPEAK 510 USB at usb-xhci-hcd.0-1, full speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x03 (3 OUT) (NONE)
    Rates: 8000, 16000, 48000
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
""".splitlines()

    _CARD3_STREAM_INFO = """\
C-Media Electronics Inc. USB Audio Device at usb-xhci-hcd.0-2, full speed : USB Audio

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
    Endpoint: 0x82 (2 IN) (SYNC)
    Rates: 48000, 44100
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501

    _CARD4_STREAM_INFO = """\
C-Media Electronics Inc. USB Audio Device at usb-xhci-hcd.1-2, full speed : USB Audio

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
    Endpoint: 0x82 (2 IN) (SYNC)
    Rates: 48000, 44100
    Bits: 16
    Channel map: MONO
""".splitlines()  # noqa: E501

    _STREAM_INFO: list[list[str]] = [
        _CARD2_STREAM_INFO,
        _CARD3_STREAM_INFO,
        _CARD4_STREAM_INFO,
    ]

    def __init__(self, card_id: int):
        super().__init__(self._STREAM_INFO[card_id])
