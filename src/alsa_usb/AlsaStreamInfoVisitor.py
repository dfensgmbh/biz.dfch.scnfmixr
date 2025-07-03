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

"""Module implementing an `MultiLineTextParserContext` ALSA stream info
visitor."""

from log import log
from text import MultiLineTextParserContext
from .AlsaStreamInfoVisitorState import AlsaStreamInfoVisitorState
from .AlsaStreamInterfaceInfo import AlsaStreamInterfaceInfo

__all__ = ["AlsaStreamInfoVisitor"]


class AlsaStreamInfoVisitor:
    """ALSA stream info visitor."""

    _playback_interfaces: list[AlsaStreamInterfaceInfo]
    _capture_interfaces: list[AlsaStreamInterfaceInfo]
    _current_interfaces: list[AlsaStreamInterfaceInfo]
    _current_interface: AlsaStreamInterfaceInfo

    def __init__(self):
        self._playback_interfaces = []
        self._capture_interfaces = []
        self._current_interfaces = None
        self._current_interface = None

    def get_interfaces(self) -> list[AlsaStreamInterfaceInfo]:
        """Returns all detected interfaces."""
        return self._playback_interfaces + self._capture_interfaces

    def get_playback_interfaces(self) -> list[AlsaStreamInterfaceInfo]:
        """Returns all detected playback interfaces."""
        return self._playback_interfaces

    def get_capture_interfaces(self) -> list[AlsaStreamInterfaceInfo]:
        """Returns all detected capture interfaces."""
        return self._capture_interfaces

    def process_playback(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Playback` section.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        log.info(
            "#%s [%s>%s] %s Processing playback interfaces ...", ctx.line, ctx.level_previous, ctx.level, ctx.keyword
        )
        self._current_interfaces = self._playback_interfaces

        return True

    def process_capture(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Capture` section.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        log.info(
            "#%s [%s>%s] %s Processing capture interfaces ...", ctx.line, ctx.level_previous, ctx.level, ctx.keyword
        )
        self._current_interfaces = self._capture_interfaces

        return True

    def process_interface(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Interface` section.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        if ctx.level_previous < ctx.level:
            return True

        self._current_interface = AlsaStreamInterfaceInfo()
        self._current_interface.state = (
            AlsaStreamInfoVisitorState.PLAYBACK
            if self._current_interfaces is self._playback_interfaces
            else AlsaStreamInfoVisitorState.CAPTURE
        )
        self._current_interfaces.append(self._current_interface)
        log.info("#%s [%s>%s] %s Prcessing interface ...", ctx.line, ctx.level_previous, ctx.level, ctx.keyword)

        return True

    def process_format(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Format` entry.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.format = result
        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.format,
        )

        return True

    def process_channels(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Channels` entry.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.channel_count = int(result)
        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.channel_count,
        )

        return True

    def process_rates(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Rates` entry.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        result = ctx.text[len(ctx.keyword) :].strip()
        try:
            self._current_interface.rates = [int(rate.strip()) for rate in result.split(",")]
        except Exception:  # pylint: disable=broad-exception-caught
            _DELIMITER = "-"
            if _DELIMITER in result:
                self._current_interface.rates = [int(result.split(_DELIMITER)[0].strip())]
            else:
                raise
        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.rates,
        )

        return True

    def process_bits(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Bits` entry.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.bit_depth = int(result)
        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.bit_depth,
        )

        return True

    def process_map(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Map` entry.
        Args:
            ctx (MultiLineTextParserContext): The parser context.
        """
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.map = [rate.strip() for rate in result.split(" ")]
        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.map,
        )

        return True
