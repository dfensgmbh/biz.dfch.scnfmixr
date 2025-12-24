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

"""Module implementing an `MultiLineTextParserContext` ALSA stream info
visitor."""

from biz.dfch.logging import log

from text import MultiLineTextParserContext
from .alsa_stream_info_visitor_state import AlsaStreamInfoVisitorState
from .alsa_stream_interface_info import AlsaStreamInterfaceInfo

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

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        log.info(
            "#%s [%s>%s] %s Processing playback interfaces ...",
            ctx.line, ctx.level_previous, ctx.level, ctx.keyword)

        self._current_interfaces = self._playback_interfaces

        return True

    def process_capture(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Capture` section.

        Args:
            ctx (MultiLineTextParserContext): The parser context.

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        log.info(
            "#%s [%s>%s] %s Processing capture interfaces ...",
            ctx.line, ctx.level_previous, ctx.level, ctx.keyword)

        self._current_interfaces = self._capture_interfaces

        return True

    def process_interface(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Interface` section.

        Args:
            ctx (MultiLineTextParserContext): The parser context.

        Returns:
            bool: True, to continue processing; false, otherwise.
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

        log.info("#%s [%s>%s] %s Prcessing interface ...",
                 ctx.line, ctx.level_previous, ctx.level, ctx.keyword)

        return True

    def process_format(self, ctx: MultiLineTextParserContext) -> bool:
        """Callback processing `Format` entry.

        Args:
            ctx (MultiLineTextParserContext): The parser context.

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        result = ctx.text[len(ctx.keyword):].strip()
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

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        result = ctx.text[len(ctx.keyword):].strip()
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

        result = ctx.text[len(ctx.keyword):].strip()

        try:
            self._current_interface.rates = [
                int(rate.strip()) for rate in result.split(",")]

        except Exception:  # pylint: disable=broad-exception-caught
            _delimiter = "-"

            if _delimiter not in result:
                raise

            self._current_interface.rates = [
                int(result.split(_delimiter)[0].strip())]

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

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        result = ctx.text[len(ctx.keyword):].strip()
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

        Returns:
            bool: True, to continue processing; false, otherwise.
        """

        _space = " "

        result = ctx.text[len(ctx.keyword):].strip()
        self._current_interface.map = [
            rate.strip() for rate in result.split(_space)]

        log.info(
            "#%s [%s>%s] %s '%s'",
            ctx.line,
            ctx.level_previous,
            ctx.level,
            ctx.keyword,
            self._current_interface.map,
        )

        return True
