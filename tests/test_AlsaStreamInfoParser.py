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

from typing import Callable
import unittest

from src.AlsaStreamInfoParser import AlsaStreamInfoParser
from src.AlsaStreamInfoParserContext import AlsaStreamInfoParserContext


class AlsaStreamInfoParserTest(unittest.TestCase):

    def test_parsing_stream_data_succeeds(self):

        # Arrange
        text = """\
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
""".splitlines()

        default: Callable[[AlsaStreamInfoParserContext], None] = lambda ctx: print(f"[#{ctx.line}][{ctx.level}] default: {ctx.keyword}")
        map = {
            "Playback:": lambda ctx: print(f"Playback: {ctx.keyword}"),
            "Capture:": lambda ctx: print(f"Capture: {ctx.keyword}"),
        }

        parser = AlsaStreamInfoParser(text, map, default)

        parser.Parse(text)


if __name__ == "__main__":
    unittest.main()
