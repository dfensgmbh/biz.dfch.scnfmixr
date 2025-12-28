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
