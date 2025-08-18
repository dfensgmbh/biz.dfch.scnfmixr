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

    # Detection of local audio device.
    INITIALISE_LCL_ENTER = auto()
    # This will be the welcome sound.
    INITIALISE_LCL_LEAVE = auto()

    # Detection of input device.
    INITIALISE_HI1_ENTER = auto()
    # This will be the welcome sound.
    INITIALISE_HI1_LEAVE = auto()

    SELECT_LANGUAGE_ENTER = auto()

    INITIALISE_EX1_ENTER = auto()
    INITIALISE_EX2_ENTER = auto()

    INITIALISE_RC1_ENTER = auto()
    INITIALISE_RC2_ENTER = auto()

    SET_DATE_ENTER = auto()
    SET_TIME_ENTER = auto()
    SET_NAME_ENTER = auto()

    INIT_AUDIO_LEAVE = auto()

    MAIN_ENTER = auto()

    SYSTEM_ENTER = auto()

    STORAGE_MANAGEMENT_ENTER = auto()

    # No specific menu.
    SWALLOW_STATE_ENTER_LEAVE = auto()
