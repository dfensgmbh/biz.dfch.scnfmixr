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

"""Module input_event_map."""

from enum import StrEnum


class InputEventMap(StrEnum):
    """Input events for state transitions."""

    KEY_ASTERISK = "*"
    KEY_HASH = "#"
    KEY_0 = "0"

    KEY_1 = "1"
    KEY_2 = "2"
    KEY_3 = "3"

    KEY_4 = "4"
    KEY_5 = "5"
    KEY_6 = "6"

    KEY_7 = "7"
    KEY_8 = "8"
    KEY_9 = "9"

    KEY_ENTER = "!"
    KEY_BACKSPACE = "£"
    KEY_TAB = "$"
