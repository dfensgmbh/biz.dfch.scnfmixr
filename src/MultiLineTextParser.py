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
from typing import Callable, Dict

from src.MultiLineTextParserContext import MultiLineTextParserContext
from src.TextUtils import TextUtils
from src.log import log


class MultiLineTextParser:
    """Parses an ALSA stream info and invokes callbacks based on parsed keywords."""

    def __init__(
        self,
        text: list[str],
        map: Dict[str, Callable[[MultiLineTextParserContext], None]],
        default: Callable[[MultiLineTextParserContext], None] = None,
    ):
        """Initialises an ALSA stream info parser.
        Args:
            text (str): An array of strings containing the ALSA stream info.
            map: A dictionary of keyword / func to be invoked when specified keywords are parsed.
            default: A default func to be invoked when no keyword is defined. Can be None.

        Returns:
            An instance of the class.
        """

        assert text is not None
        assert map is not None

        self.text = text
        self.map = map
        self.default = default

    @staticmethod
    def get_stream_info_data(id: int) -> list[str]:
        """Reads stream data from `stream0` for a given ALSA card id and returns an array of strings.
        Throws an exception if no `stream0` file exists.

        Args:
            id (int): The ALSA card id.

        Returns:
            Returns stream info as a list of strings.
        """

        assert id >= 0

        PROC_ASOUND_BASEPATH = "/proc/asound/"
        STREAM_FILE = "stream0"

        card_path = f"{PROC_ASOUND_BASEPATH}card{id}"
        card_stream_file = os.path.join(card_path, STREAM_FILE)

        return TextUtils().read_all_lines(card_stream_file)

    def Parse(self, stream_info_data: list[str]) -> None:
        """Parses specified stream info data.

        Args:
            stream_info_data (list[str]): An array of strings containing stream
                info data as returned by `get_stream_info_data`.

        Returns:
            None. This method does not return anything.
        """

        assert stream_info_data is not None

        ctx = MultiLineTextParserContext()

        for line in stream_info_data:
            ctx.line += 1

            # Skip empty lines.
            if line is None or "" == line.strip():
                continue

            # Ensure we have an even spacing.
            leading_spaces = len(line) - len(line.lstrip(" "))
            assert 0 == leading_spaces % 2, f"[{ctx.level}] Invalid spacing on #{line} '{line}' [{leading_spaces}]."

            # Upate indentation.
            ctx.level_previous = ctx.level
            ctx.level = int(leading_spaces / 2)

            # Now parse the actual line.
            ctx.text = line.strip()

            # Find function to call on keyword.
            func = None
            ctx.keyword = None
            for key in sorted(self.map.keys(), key=len, reverse=True):
                if ctx.text.startswith(key):
                    func = self.map[key]
                    ctx.keyword = key
                    break

            # Or use default func if not keyword matches.
            if func is None and self.default is not None:
                func = self.default

            if func is not None:
                # Invoke function.
                log.debug(f"Invoke '{ctx.keyword}' on '{ctx.text}'.")
                func(replace(ctx))
