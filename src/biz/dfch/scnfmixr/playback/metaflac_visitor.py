# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

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

"""Module metaflac_visitor."""

import re

from biz.dfch.logging import log
from text import MultiLineTextParserContext


class MetaflacVisitor:
    """Implements a parser for `metaflac --list`.

    Works with metaflac **v1.4.2**.
    """

    METADATA_BLOCK = "METADATA block #"
    STREAM_INFO = "type: 0 (STREAMINFO)"
    SAMPLE_RATE = "sample_rate: "
    SEEK_TABLE = "type: 3 (SEEKTABLE)"
    SEEK_POINT = "point "

    _is_in_stream_info: bool
    _is_in_seek_table: bool

    sample_rate: int
    items: list[int]

    def __init__(self):

        self.sample_rate = 0
        self.items = []
        self._is_in_stream_info = False
        self._is_in_seek_table = False

    def process_metadata_block(self, ctx: MultiLineTextParserContext) -> bool:
        """METADATA block #"""

        assert isinstance(ctx, MultiLineTextParserContext)

        self._is_in_stream_info = False
        self._is_in_seek_table = False

        return True

    def process_stream_info(self, ctx: MultiLineTextParserContext) -> bool:
        """type: 0 (STREAMINFO)"""

        assert isinstance(ctx, MultiLineTextParserContext)

        self._is_in_stream_info = True

        return True

    def process_sample_rate(self, ctx: MultiLineTextParserContext) -> bool:
        """sample_rate: """

        assert isinstance(ctx, MultiLineTextParserContext)

        log.debug("Sample rate '%s': '%s'", ctx.keyword, ctx.text)

        match = re.search(r'\b(\d+)\b', ctx.text)

        if not match:
            self.sample_rate = 0
            log.warning("Sample rate '%s' FAILED: '%s'", ctx.keyword, ctx.text)

            return False

        value = int(match.group(1))
        self.sample_rate = value
        log.info("Sample rate '%s' OK: '%s'", ctx.keyword, value)

        return True

    def process_seek_table(self, ctx: MultiLineTextParserContext) -> bool:
        """type: 3 (SEEKTABLE)"""

        assert isinstance(ctx, MultiLineTextParserContext)

        self._is_in_seek_table = True

        return True

    def process_seek_point(self, ctx: MultiLineTextParserContext) -> bool:
        """point """

        assert isinstance(ctx, MultiLineTextParserContext)

        log.debug("Seek point '%s': '%s'", ctx.keyword, ctx.text)

        if 0 == self.sample_rate:
            log.warning("Seek point '%s' FAILED: '%s'. Sample rate is 0.",
                        ctx.keyword, ctx.text)

            return False

        match = re.search(r'sample_number=(\d+)', ctx.text)
        if not match:
            log.warning("Seek point '%s' FAILED: '%s'.",
                        ctx.keyword, ctx.text)
            return False

        value = int(match.group(1))
        seconds = int(value / self.sample_rate)

        self.items.append(seconds)

        log.info("Seek point '%s' OK: '%s'", ctx.keyword, seconds)

        return True
