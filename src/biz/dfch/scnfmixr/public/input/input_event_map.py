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

    # KEY_ENTER = "⏎"  # \u23ce
    # KEY_ENTER = "↵"  # \u21b5
    # KEY_BACKSPACE = "⌫"  # \u232b
    # KEY_TAB = "⇥"  # \u21e4
