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

from dataclasses import dataclass, field
from typing import Any

from .alsa_stream_info_visitor_state import AlsaStreamInfoVisitorState

__all__ = ["AlsaStreamInterfaceInfo"]


@dataclass
class AlsaStreamInterfaceInfo:
    """Contains information about an ALSA stream interface.

    state (AlsaStreamInfoVisitorState): The state of the interface.
    format (str): Supported format of interface.
    channel_count (int): Supported channel count of interface.
    bit_depth (int): Supported bit depth of interface.
    map (list[str]): ???
    rates (list[int]): Available sample rates of interface.
    """

    state: AlsaStreamInfoVisitorState = AlsaStreamInfoVisitorState.DEFAULT
    format: str = None
    channel_count: int = 0
    bit_depth: int = 0
    map: list[str] = field(default_factory=list)
    rates: list[int] = field(default_factory=list)

    def get_best_rate(self) -> int:
        """Returns the best sampling rate from a list of sampling rates."""

        return max((r for r in self.rates if r <= 48000), default=0)

    def to_dict(self) -> dict[str, Any]:
        """Converts ALSA stream information into a dictionary.

        Returns:
            Dict (str, Any): A key-value map containing the ALSA stream
                information.
        """

        result = {
            "state": self.state,
            "format": self.format,
            "channels": self.channel_count,
            "bit_depth": self.bit_depth,
            "map": self.map,
            "rates": self.rates,
        }

        return result
