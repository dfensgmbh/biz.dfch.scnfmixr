# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

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

        assert 0 < self.card_id
        assert 0 <= self.interface_id
        assert self.format in Format
        assert 1 <= self.channel_count
        assert self.sample_rate in SampleRate
        assert self.bit_depth in BitDepth
