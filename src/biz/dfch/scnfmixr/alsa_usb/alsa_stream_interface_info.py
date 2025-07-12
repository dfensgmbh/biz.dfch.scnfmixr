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
