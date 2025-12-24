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


from __future__ import annotations
from dataclasses import replace
import re
from typing import Callable

from biz.dfch.logging import log

from .MultiLineTextParserContext import MultiLineTextParserContext

__all__ = [
    "MultiLineTextParser",
    "MultiLineTextParserMap",
    "MultiLineTextParserFunc",
]

MultiLineTextParserFunc = Callable[[MultiLineTextParserContext], bool]
MultiLineTextParserMap = dict[str, MultiLineTextParserFunc]


class MultiLineTextParser:
    """Parses an ALSA stream info and invokes callbacks based on parsed
    keywords.

    Attributes:
        indent (str): The indentation character.
        length (int): The indentation per hierarchy level.
        dic (MultiLineTextParserMap): A dictionary of keyword / func to be
            invoked when specified keywords are parsed.
        default (MultiLineTextParserFunc | None): A default func to be
            invoked when no keyword is defined. Can be None.
    """

    indent: str
    length: int
    dic: MultiLineTextParserMap
    default: MultiLineTextParserFunc | None

    def __init__(
        self,
        indent: str,
        length: int,
        dic: MultiLineTextParserMap,
        default: MultiLineTextParserFunc = None,
    ) -> None:
        """Initialises an ALSA stream info parser.
        Args:
            indent (str): The indentation character.
            length (int): The indentation per hierarchy level.
            dic (MultiLineTextParserMap): A dictionary of keyword / func to be
                invoked when specified keywords are parsed.
            default (MultiLineTextParserFunc | None): A default func to be
                invoked when no keyword is defined. Can be None.
        """

        assert indent is not None and 1 == len(indent)
        assert 0 <= length
        assert dic is not None

        self.indent = indent
        self.length = length
        self.dic = dic
        self.default = default

    # # DFTODO - must be moved out of this class.
    # @staticmethod
    # def get_stream_info_data(idx: int) -> list[str]:
    #     """Reads stream data from `stream0` for a given ALSA card id and
    #     returns an array of strings.

    #     Args:
    #         idx (int): The ALSA card id.

    #     Returns:
    #         Returns stream info as a list of strings.

    #     Raises:
    #         Exception: Throws an exception if `stream0` does not exist.
    #     """

    #     assert idx >= 0

    #     PROC_ASOUND_BASEPATH = "/proc/asound/"
    #     STREAM_FILE = "stream0"

    #     card_path = f"{PROC_ASOUND_BASEPATH}card{idx}"
    #     card_stream_file = os.path.join(card_path, STREAM_FILE)

    #     return TextUtils().read_all_lines(card_stream_file)

    def parse(self, value: list[str], is_regex: bool = False) -> None:
        """Parses specified stream info data.

        Args:
            value (list[str]): An array of strings containing lines of text.
            is_regex (bool): True, if the keywords are regex; false otherwise
                (default).

        Returns:
            None
        """

        assert value is not None

        ctx = MultiLineTextParserContext()

        for line in value:
            ctx.line += 1

            # Skip empty lines.
            if line is None or "" == line.strip():
                continue

            # Ensure we have an even spacing.
            leading_indent = len(line) - len(line.lstrip(self.indent))
            assert 0 == leading_indent % self.length

            # Upate indentation.
            ctx.level_previous = ctx.level
            ctx.level = int(leading_indent / self.length)

            # Now parse the actual line.
            ctx.text = line.strip()

            # Find function to call on keyword.
            func = None
            ctx.keyword = None
            for key in sorted(self.dic.keys(), key=len, reverse=True):

                if (
                    re.search(key, ctx.text)
                    if is_regex else ctx.text.startswith(key)
                ):
                    ctx.keyword = key
                    func = self.dic[key]
                    break

            # Or use default func if not keyword matches.
            if func is None and self.default is not None:
                func = self.default

            if func is not None:
                # Invoke function.
                log.debug("Invoke '%s' on '%s'.", ctx.keyword, ctx.text)

                result = func(replace(ctx))
                if not result:
                    return
