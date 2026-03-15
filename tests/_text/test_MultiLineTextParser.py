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

import unittest

from biz.dfch.logging import log

from text import MultiLineTextParser, MultiLineTextParserContext


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

        def process_default(ctx: MultiLineTextParserContext) -> bool:
            log.debug(
                "[#%s][%s>%s] default: %s",
                ctx.line,
                ctx.level_previous,
                ctx.level,
                ctx.text)
            return True

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

        def increment_call_count(
                ctx: MultiLineTextParserContext, key: str) -> bool:
            _ = ctx
            counters[key] += 1
            return True

        dic = {
            "Playback:": lambda ctx: increment_call_count(ctx, "playback"),
            "Capture:": lambda ctx: increment_call_count(ctx, "capture"),
            "Interface ": lambda ctx: increment_call_count(ctx, "interface"),
            "Format:": lambda ctx: increment_call_count(ctx, "format"),
            "Channels:": lambda ctx: increment_call_count(ctx, "channels"),
            "Rates:": lambda ctx: increment_call_count(ctx, "rates"),
            "Bits:": lambda ctx: increment_call_count(ctx, "bits"),
            "Channel map:": lambda ctx: increment_call_count(ctx, "map"),
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=2,
            dic=dic,
            default=process_default)

        # Act
        parser.parse(text)

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
