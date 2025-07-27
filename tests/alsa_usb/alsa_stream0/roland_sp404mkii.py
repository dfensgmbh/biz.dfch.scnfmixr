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

"""0582:0281 Roland Corp. SP-404MKII, 0582:02e7 Roland Corp. Roland SP-404MKII

Bus 003 Device 012: ID 0582:0281 Roland Corp. SP-404MKII
Bus 003 Device 013: ID 0582:02e7 Roland Corp. Roland SP-404MKII


 5 [SP404MKII      ]: USB-Audio - SP-404MKII
                      Roland SP-404MKII at usb-xhci-hcd.1-1.4.2, full speed
"""

INFO = """\
Roland SP-404MKII at usb-xhci-hcd.1-1.4.2, full speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 4
    Endpoint: 0x0d (13 OUT) (ADAPTIVE)
    Rates: 48000
    Bits: 16
    Channel map: FL FR RL RR

Capture:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x8e (14 IN) (ASYNC)
    Rates: 48000
    Bits: 16
    Channel map: FL FR
""".splitlines()  # noqa: E501 # pylint: disable=C0301
