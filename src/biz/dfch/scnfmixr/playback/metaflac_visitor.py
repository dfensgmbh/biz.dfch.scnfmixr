# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
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
