# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
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

"""Module alsa_inferface_info."""

from dataclasses import dataclass

from .sample_rate import SampleRate
from .format import Format
from .bit_depth import BitDepth


@dataclass(frozen=True)
class AlsaInterfaceInfo:
    """Audio parameters of card and interface.

    Attributes:
        card_id (int): The ALSA card id.
        interface_id (int): The interface id of the card.
        format (Format): The format of the interface.
        channel_count (int): The number of channels of the interface.
        sample_rate (SampleRate): The sample rate of the interface.
        bit_depth (BitDepth): The bit depth of the interface.
    """

    card_id: int
    interface_id: int = 0
    format: Format = Format.DEFAULT
    channel_count: int = 1
    sample_rate: SampleRate = SampleRate.DEFAULT
    bit_depth: BitDepth = BitDepth.DEFAULT

    def __post_init__(self):

        assert 0 <= self.card_id
        assert 0 <= self.interface_id
        assert self.format in Format
        assert 1 <= self.channel_count
        assert self.sample_rate in SampleRate
        assert self.bit_depth in BitDepth
