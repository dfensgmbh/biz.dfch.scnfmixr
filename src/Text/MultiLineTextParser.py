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


from dataclasses import replace
import os
import re
from typing import Callable, Dict

from biz.dfch.logging import log

from .MultiLineTextParserContext import MultiLineTextParserContext
from .TextUtils import TextUtils

__all__ = ["MultiLineTextParser"]


class MultiLineTextParser:
    """Parses an ALSA stream info and invokes callbacks based on parsed
    keywords."""

    def __init__(
        self,
        indent: str,
        length: int,
        dic: Dict[str, Callable[[MultiLineTextParserContext], bool]],
        default: Callable[[MultiLineTextParserContext], bool] = None,
    ):
        """Initialises an ALSA stream info parser.
        Args:
            dic: A dictionary of keyword / func to be invoked when specified
                keywords are parsed.
            default: A default func to be invoked when no keyword is defined.
                Can be None.

        Returns:
            An instance of the class.
        """

        assert indent is not None and 1 == len(indent)
        assert 0 <= length
        assert dic is not None

        self.indent = indent
        self.length = length
        self.dic = dic
        self.default = default

    # DFTODO - must be moved out of this class.
    @staticmethod
    def get_stream_info_data(idx: int) -> list[str]:
        """Reads stream data from `stream0` for a given ALSA card id and
        returns an array of strings.

        Args:
            idx (int): The ALSA card id.

        Returns:
            Returns stream info as a list of strings.

        Raises:
            Exception: Throws an exception if `stream0` does not exist.
        """

        assert idx >= 0

        PROC_ASOUND_BASEPATH = "/proc/asound/"
        STREAM_FILE = "stream0"

        card_path = f"{PROC_ASOUND_BASEPATH}card{idx}"
        card_stream_file = os.path.join(card_path, STREAM_FILE)

        return TextUtils().read_all_lines(card_stream_file)

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
