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

from text import MultiLineTextParser, MultiLineTextParserContext
from log import log


class MultiLineTextParserTest(unittest.TestCase):

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

        default: Callable[[MultiLineTextParserContext], None] = lambda ctx: log.debug(
            f"[#{ctx.line}][{ctx.level_previous}>{ctx.level}] default: {ctx.text}"
        )

        counters = {
            "playback": 0,
            "capture": 0,
            "interface": 0,
            "format": 0,
            "channels": 0,
            "rates": 0,
            "bits": 0,
            "map": 0,
        }

        def increment_call_count(ctx: MultiLineTextParserContext, key: str):
            counters[key] += 1

        map = {
            "Playback:": lambda ctx: increment_call_count(ctx, "playback"),
            "Capture:": lambda ctx: increment_call_count(ctx, "capture"),
            "Interface ": lambda ctx: increment_call_count(ctx, "interface"),
            "Format:": lambda ctx: increment_call_count(ctx, "format"),
            "Channels:": lambda ctx: increment_call_count(ctx, "channels"),
            "Rates:": lambda ctx: increment_call_count(ctx, "rates"),
            "Bits:": lambda ctx: increment_call_count(ctx, "bits"),
            "Channel map:": lambda ctx: increment_call_count(ctx, "map"),
        }

        parser = MultiLineTextParser(text, map, default)

        # Act
        parser.Parse(text)

        # Assert
        self.assertEqual(counters["playback"], 1)
        self.assertEqual(counters["capture"], 1)
        self.assertEqual(counters["interface"], 3)
        self.assertEqual(counters["format"], 3)
        self.assertEqual(counters["channels"], 3)
        self.assertEqual(counters["rates"], 3)
        self.assertEqual(counters["bits"], 3)
        self.assertEqual(counters["map"], 3)


if __name__ == "__main__":
    unittest.main()
