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

from .AlsaStreamInfoVisitorState import AlsaStreamInfoVisitorState
from .AlsaStreamInterfaceInfo import AlsaStreamInterfaceInfo
from log import log
from text import MultiLineTextParserContext

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
        return self._playback_interfaces + self._capture_interfaces

    def get_playback_interfaces(self) -> list[AlsaStreamInterfaceInfo]:
        return self._playback_interfaces

    def get_capture_interfaces(self) -> list[AlsaStreamInterfaceInfo]:
        return self._capture_interfaces

    def process_playback(self, ctx: MultiLineTextParserContext) -> None:
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} Processing playback interfaces ...")
        self._current_interfaces = self._playback_interfaces

    def process_capture(self, ctx: MultiLineTextParserContext) -> None:
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} Processing capture interfaces ...")
        self._current_interfaces = self._capture_interfaces

    def process_interface(self, ctx: MultiLineTextParserContext) -> None:
        if ctx.level_previous < ctx.level:
            return

        self._current_interface = AlsaStreamInterfaceInfo()
        self._current_interface.state = (
            AlsaStreamInfoVisitorState.PLAYBACK
            if self._current_interfaces is self._playback_interfaces
            else AlsaStreamInfoVisitorState.CAPTURE
        )
        self._current_interfaces.append(self._current_interface)
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword}Creating interface ...")

    def process_format(self, ctx: MultiLineTextParserContext) -> None:
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.format = result
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} '{self._current_interface.format}'")

    def process_channels(self, ctx: MultiLineTextParserContext) -> None:
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.channel_count = int(result)
        log.info(
            f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} '{self._current_interface.channel_count}'"
        )

    def process_rates(self, ctx: MultiLineTextParserContext) -> None:
        result = ctx.text[len(ctx.keyword) :].strip()
        try:
            self._current_interface.rates = [int(rate.strip()) for rate in result.split(",")]
        except Exception:
            DELIMITER = "-"
            if DELIMITER in result:
                self._current_interface.rates = [int(result.split(DELIMITER)[0].strip())]
            else:
                raise
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} '{self._current_interface.rates}'")

    def process_bits(self, ctx: MultiLineTextParserContext) -> None:
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.bit_depth = int(result)
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} '{self._current_interface.bit_depth}'")

    def process_map(self, ctx: MultiLineTextParserContext) -> None:
        result = ctx.text[len(ctx.keyword) :].strip()
        self._current_interface.map = [rate.strip() for rate in result.split(" ")]
        log.info(f"#{ctx.line} [{ctx.level_previous}>{ctx.level}] {ctx.keyword} '{self._current_interface.map}'")
