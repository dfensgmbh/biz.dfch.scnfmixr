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

"""Module connection_policy."""

from enum import Enum, auto


class ConnectionPolicy(Enum):
    """Strategy for connecting signal sets to other signal sets.

    Attributes:
        MONO: Connects the first source point to the first sink point. When
            connecting sets only the first point in the source set is connected
            to the first point in the sink set.

            Valid between any combination of points and sets.
        DUAL: Connect the first two source points to the first two sink points,
            or, if source is a point, connect the source point to the first two
            sink points.

            Source can be point or set, sink must be a set.
        LINE: When source point count equals sink point count, connect source
            source points index-wise to sink points.

            If source and sink counts equals 1, it behaves like MONO.

            Valid between any combination of points and sets, as long as point
            count equals.
        BCAST: Will connect the first source point to all other sink points. If
            sink is a point, BCAST will behave like MONO.

            Valid between any combination of points and sets.

            *This is the opposite behaviour of MERGE.*
        MERGE: Connects all source points to the first sink point. If source is
            a point, MERGE will behave like MONO.

            Valid between any combination of points and sets.

            *This is the opposite behaviour of BCAST.*
        TRUNC: Connects as many source points to as many sink points as
            possible. If source count is greater than sink count, not all source
            points will be connected. If source count is less than sink count,
            not all sink points will be connected.

            Valid between any combination of points and sets.
        DEFAULT: Will connect in the following order:
            * source count == sink count == 1: MONO, LINE
            * source count ==  1 and sink count != 1: BCAST
            * source count !=  1 and sink count == 1: MERGE
            * source count > sink count: TRUNC
            * source count < sink count: TRUNC

            Valid between any combination of points and sets.
    """
    DEFAULT = auto()
    MONO = auto()
    DUAL = auto()
    LINE = auto()
    BCAST = auto()
    MERGE = auto()
    TRUNC = auto()
