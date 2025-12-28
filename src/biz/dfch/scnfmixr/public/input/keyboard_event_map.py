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

"""Module key_event_map"""

from enum import StrEnum

from .input_event_map import InputEventMap


class KeyboardEventMap(StrEnum):
    """Maps keyboard key codes to state machine events.

    Be cautious when defining entries for `KEY_KPPLUS` and similar. These will
    only work on a numeric keypad and not on the main part of the keyboard (as
    only the scan code are processed (and not keys in combination like SHIFT).
    """

    KEY_KP0 = InputEventMap.KEY_0
    KEY_0 = InputEventMap.KEY_0

    KEY_KP1 = InputEventMap.KEY_1
    KEY_1 = InputEventMap.KEY_1
    KEY_KP2 = InputEventMap.KEY_2
    KEY_2 = InputEventMap.KEY_2
    KEY_KP3 = InputEventMap.KEY_3
    KEY_3 = InputEventMap.KEY_3

    KEY_KP4 = InputEventMap.KEY_4
    KEY_4 = InputEventMap.KEY_4
    KEY_KP5 = InputEventMap.KEY_5
    KEY_5 = InputEventMap.KEY_5
    KEY_KP6 = InputEventMap.KEY_6
    KEY_6 = InputEventMap.KEY_6

    KEY_7 = InputEventMap.KEY_7
    KEY_KP7 = InputEventMap.KEY_7
    KEY_8 = InputEventMap.KEY_8
    KEY_KP8 = InputEventMap.KEY_8
    KEY_9 = InputEventMap.KEY_9
    KEY_KP9 = InputEventMap.KEY_9

    KEY_KPENTER = InputEventMap.KEY_ENTER
    KEY_ENTER = InputEventMap.KEY_ENTER

    KEY_DOT = "."
    KEY_KPDOT = "."

    KEY_KPPLUS = "+"
    KEY_KPMINUS = "-"
    KEY_KPASTERISK = InputEventMap.KEY_ASTERISK
    KEY_KPSLASH = "/"
    KEY_EQUAL = "="

    KEY_TAB = InputEventMap.KEY_TAB
    KEY_BACKSPACE = InputEventMap.KEY_BACKSPACE

    KEY_NUMLOCK = "?"
