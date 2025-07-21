# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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
