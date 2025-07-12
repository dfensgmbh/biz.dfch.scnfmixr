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

"""Sound Devices MixPre-6 II"""  # noqa: E501 # pylint: disable=C0301

INFO = """\
Sound Devices, LLC MixPre-6 II at usb-xhci-hcd.0-2, high speed : USB Audio

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
""".splitlines()
