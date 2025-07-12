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
