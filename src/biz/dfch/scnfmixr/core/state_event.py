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

"""Module state_event."""

from enum import StrEnum, auto


class StateEvent(StrEnum):
    """State Enter and Leave audio information."""

    INITIALISE_HI1_ENTER = auto()
    INITIALISE_HI1_LEAVE = auto()
    INITIALISE_HI2_ENTER = auto()
    INITIALISE_HI2_LEAVE = auto()
    INITIALISE_HI3_ENTER = auto()
    INITIALISE_HI3_LEAVE = auto()

    INITIALISE_LCL_ENTER = auto()
    INITIALISE_LCL_LEAVE = auto()
    INITIALISE_EX1_ENTER = auto()
    INITIALISE_EX1_LEAVE = auto()
    INITIALISE_EX2_ENTER = auto()
    INITIALISE_EX2_LEAVE = auto()

    INITIALISE_RC1_ENTER = auto()
    INITIALISE_RC1_LEAVE = auto()
    INITIALISE_RC2_ENTER = auto()
    INITIALISE_RC2_LEAVE = auto()

    SELECT_LANGUAGE_ENTER = auto()
    SELECT_LANGUAGE_LEAVE = auto()

    SET_DATE_ENTER = auto()
    SET_DATE_LEAVE = auto()
    SET_TIME_ENTER = auto()
    SET_TIME_LEAVE = auto()
    SET_NAME_ENTER = auto()
    SET_NAME_LEAVE = auto()

    INIT_AUDIO_ENTER = auto()
    INIT_AUDIO_LEAVE = auto()

    SYSTEM_MENU_ENTER = auto()
    SYSTEM_MENU_LEAVE = auto()

    RECORD_ENTER = auto()
    RECORD_LEAVE = auto()
    ONRECORD_ENTER = auto()
    ONRECORD_LEAVE = auto()

    PLAYBACK_ENTER = auto()
    PLAYBACK_LEAVE = auto()

    FINAL_STATE_ENTER = auto()
    FINAL_STATE_LEAVE = auto()
