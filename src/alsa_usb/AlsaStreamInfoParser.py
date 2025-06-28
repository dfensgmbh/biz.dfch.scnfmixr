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

"""Implements a `MultiLineTextParser` for parsing ALSA stream information."""

from text import MultiLineTextParser, TextUtils
from .AlsaStreamInfoVisitor import AlsaStreamInfoVisitor
from .AlsaStreamInterfaceInfo import AlsaStreamInterfaceInfo


class AlsaStreamInfoParser(MultiLineTextParser):
    """Implements a `MultiLineTextParser` for parsing ALSA stream information.
    """

    def __init__(self, id_card: int):

        assert 0 <= id_card

        stream_fullname = f"/proc/asound/card{id_card}/stream0"
        text = TextUtils().read_all_lines(stream_fullname)

        visitor = AlsaStreamInfoVisitor()
        callbacks = {
            "Playback:": visitor.process_playback,
            "Capture:": visitor.process_capture,
            "Interface ": visitor.process_interface,
            "Format:": visitor.process_format,
            "Channels:": visitor.process_channels,
            "Rates:": visitor.process_rates,
            "Bits:": visitor.process_bits,
            "Channel map:": visitor.process_map,
        }

        super().__init__(text, callbacks)
        super().Parse(text)

        self.visitor = visitor

    def get_best_capture_interface(self) -> AlsaStreamInterfaceInfo | None:
        """Selects the best capture interface."""

        candidates = [
            interface
            for interface in self.visitor.get_capture_interfaces()
            if interface.bit_depth != 0
            and 1 <= interface.channel_count <= 2
            and any(rate % 16000 == 0 or rate == 44100 for rate in
                    interface.rates)
        ]

        result = next(
            iter(
                sorted(
                    candidates,
                    key=lambda i: (
                        -self.best_rate(i.rates),
                        -i.channel_count,
                        i.format
                    )
                )
            ),
            None
        )
        return result

    def get_best_playback_interface(self) -> AlsaStreamInterfaceInfo | None:
        """Selects the best playback interface."""

        candidates = [
            interface
            for interface in self.visitor.get_playback_interfaces()
            if interface.bit_depth != 0
            and 1 <= interface.channel_count <= 2
            and any(rate % 16000 == 0 or rate == 44100 for rate in
                    interface.rates)
        ]

        result = next(
            iter(
                sorted(
                    candidates,
                    key=lambda i: (
                        -self.best_rate(i.rates),
                        -i.channel_count,
                        i.format
                    )
                )
            ),
            None
        )
        return result

    def best_rate(self, rates: list[int]) -> int:
        """Returns the best sampling rate from a list of sampling rates."""
        return max((r for r in rates if r <= 48000), default=0)
