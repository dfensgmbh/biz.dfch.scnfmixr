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

"""Implements a parser for ALSA stream information."""

from typing import overload

from text import MultiLineTextParser, TextUtils

from .alsa_stream_info_visitor import AlsaStreamInfoVisitor
from .alsa_stream_interface_info import AlsaStreamInterfaceInfo


class AlsaStreamInfoParser(MultiLineTextParser):
    """Implements a parser for ALSA stream information."""

    _indent: str
    _spacing: int

    interface_id: int

    @overload
    def __init__(self, card_id: int) -> None:
        ...

    @overload
    def __init__(self, contents: list[str]) -> None:
        ...

    def __init__(self, value: int | list[str]) -> None:
        """Creates an ALSA stream info parser.

        Args:
            value (int, list[str]): Either the ALSA id of the sound card or the
                contents of an ALSA stream info file as a list of strings.
        """

        self._indent = " "
        self._spacing = 2

        assert value
        assert isinstance(value, (int, list))

        self.interface_id = 0

        text = value
        if isinstance(value, int):
            id_card = value
            assert 0 <= id_card

            stream_fullname = (
                f"/proc/asound/card{id_card}/"
                f"stream{self.interface_id}")
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

        super().__init__(
            indent=self._indent, length=self._spacing, dic=callbacks)
        super().parse(text)

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
        """Returns the best sampling rate from a list of sampling rates.

        **DEPRECATED**: Do not use this method. Instead use `get_best_rate()`
        from capture or playback interface.
        """
        return max((r for r in rates if r <= 48000), default=0)
