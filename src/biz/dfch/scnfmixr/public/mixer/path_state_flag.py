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

"""Module path_state_flag."""

from enum import IntFlag


class PathStateFlag(IntFlag):
    """The states of a path."""
    INITIAL = 0x01
    OK = 0x02
    STALE = 0x04
    REMOVED = 0x08
    ACQUIRED = 0x80

    RELEASED_INITIAL = INITIAL
    RELEASED_OK = OK
    RELEASED_STALE = STALE
    RELEASED_REMOVED = REMOVED
    ACQUIRED_INITIAL = ACQUIRED | INITIAL
    ACQUIRED_OK = ACQUIRED | OK
    ACQUIRED_STALE = ACQUIRED | STALE
    ACQUIRED_REMOVE = ACQUIRED | REMOVED
