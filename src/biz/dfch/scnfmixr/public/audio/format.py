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

"""Module format."""

from enum import StrEnum

from .bit_depth import BitDepth


class Format(StrEnum):
    """Audio encoding format."""

    S16_LE = "S16_LE"
    S24_LE = "S24_LE"
    S24_3LE = "S24_3LE"
    S32_LE = "S32_LE"
    FLOAT_LE = "FLOAT_LE"
    DEFAULT = S24_3LE

    def get_bit_depth(self) -> int:
        """Returns the bit depth of a format."""

        match self:
            case Format.S16_LE:
                return BitDepth.B16
            case Format.S24_LE | Format.S24_3LE:
                return BitDepth.B24
            case Format.S32_LE:
                return BitDepth.B32
            case _:
                raise LookupError
