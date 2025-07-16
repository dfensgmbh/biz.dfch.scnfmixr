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

"""Module transition_event."""

from enum import StrEnum, auto


class TransitionEvent(StrEnum):
    """Transition Enter and Leave audio information."""

    # Menu: Detect HID HI1.
    DETECTING_DEVICE_HI1_ENTER = auto()
    DETECTING_DEVICE_HI1_LEAVE = auto()
    SKIPPING_DEVICE_HI1_ENTER = auto()
    SKIPPING_DEVICE_HI1_LEAVE = auto()

    # Menu: Detect HID HI2.
    DETECTING_DEVICE_HI2_ENTER = auto()
    DETECTING_DEVICE_HI2_LEAVE = auto()
    SKIPPING_DEVICE_HI2_ENTER = auto()
    SKIPPING_DEVICE_HI2_LEAVE = auto()

    # Menu: Detect HID HI3.
    DETECTING_DEVICE_HI3_ENTER = auto()
    DETECTING_DEVICE_HI3_LEAVE = auto()
    SKIPPING_DEVICE_HI3_ENTER = auto()
    SKIPPING_DEVICE_HI3_LEAVE = auto()

    # Menu: Detect Audio LCL.
    DETECTING_DEVICE_LCL_ENTER = auto()
    DETECTING_DEVICE_LCL_LEAVE = auto()
    SKIPPING_DEVICE_LCL_ENTER = auto()
    SKIPPING_DEVICE_LCL_LEAVE = auto()

    # Menu: Detect Audio EX1.
    DETECTING_DEVICE_EX1_ENTER = auto()
    DETECTING_DEVICE_EX1_LEAVE = auto()
    SKIPINNG_DEVICE_EX1_ENTER = auto()
    SKIPINNG_DEVICE_EX1_LEAVE = auto()

    # Menu: Detect Audio EX2.
    DETECTING_DEVICE_EX2_ENTER = auto()
    DETECTING_DEVICE_EX2_LEAVE = auto()
    SKIPINNG_DEVICE_EX2_ENTER = auto()
    SKIPINNG_DEVICE_EX2_LEAVE = auto()

    # Menu: Detect storage RC1.
    DETECTING_DEVICE_RC1_ENTER = auto()
    DETECTING_DEVICE_RC1_LEAVE = auto()
    SKIPPING_DEVICE_RC1_ENTER = auto()
    SKIPPING_DEVICE_RC1_LEAVE = auto()

    # Menu: Detect storage RC2.
    DETECTING_DEVICE_RC2_ENTER = auto()
    DETECTING_DEVICE_RC2_LEAVE = auto()
    SKIPPING_DEVICE_RC2_ENTER = auto()
    SKIPPING_DEVICE_RC2_LEAVE = auto()

    # Menu: Clean storage RC1.
    CLEANING_DEVICE_RC1_ENTER = auto()
    CLEANING_DEVICE_RC1_LEAVE = auto()

    # Menu: Clean storage RC1.
    CLEANING_DEVICE_RC2_ENTER = auto()
    CLEANING_DEVICE_RC2_LEAVE = auto()

    # Menu: Select language.
    SELECTING_ENGLISH_ENTER = auto()
    SELECTING_ENGLISH_LEAVE = auto()
    SELECTING_GERMAN_ENTER = auto()
    SELECTING_GERMAN_LEAVE = auto()
    SELECTING_FRENCH_ENTER = auto()
    SELECTING_FRENCH_LEAVE = auto()
    SELECTING_ITALIAN_ENTER = auto()
    SELECTING_ITALIAN_LEAVE = auto()

    # Menu: Initialise audio.
    INITIALISING_AUDIO_ENTER = auto()
    INITIALISING_AUDIO_LEAVE = auto()

    # Menu: Record.
    STARTING_RECORDING_ENTER = auto()
    STARTING_RECORDING_LEAVE = auto()
    SETTING_DATE_ENTER = auto()
    SETTING_DATE_LEAVE = auto()
    MOUNTING_STORAGE_ENTER = auto()
    MOUNTING_STORAGE_LEAVE = auto()
    DISCONNECTING_STORAGE_ENTER = auto()
    DISCONNECTING_STORAGE_LEAVE = auto()
    STOPPING_SYSTEM_ENTER = auto()
    STOPPING_SYSTEM_LEAVE = auto()

    # Menu: OnRecord.
    STOPPING_RECORDING_ENTER = auto()
    STOPPING_RECORDING_LEAVE = auto()
    SETTING_CUEPOINT_ENTER = auto()
    SETTING_CUEPOINT_LEAVE = auto()
    TOGGLING_MUTE_ENTER = auto()
    TOGGLING_MUTE_LEAVE = auto()
    SHOWING_STATUS_ENTER = auto()
    SHOWING_STATUS_LEAVE = auto()

    # Menu: Date, Time, Name
    PROCESSING_DIGIT_ENTER = auto()
    PROCESSING_DIGIT_LEAVE = auto()
