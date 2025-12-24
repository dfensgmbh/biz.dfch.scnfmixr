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

"""Module transition_event."""

from enum import StrEnum, auto


class TransitionEvent(StrEnum):
    """Transition Enter and Leave audio information."""

    # Menu: Detect HID HI1.
    DETECTING_DEVICE_HI1_ENTER = auto()
    DETECTING_DEVICE_HI1_LEAVE = auto()
    SKIPPING_DEVICE_HI1_LEAVE = auto()

    # Menu: Detect HID HI2.
    DETECTING_DEVICE_HI2_ENTER = auto()
    DETECTING_DEVICE_HI2_LEAVE = auto()
    SKIPPING_DEVICE_HI2_LEAVE = auto()

    # Menu: Detect HID HI3.
    DETECTING_DEVICE_HI3_ENTER = auto()
    DETECTING_DEVICE_HI3_LEAVE = auto()
    SKIPPING_DEVICE_HI3_LEAVE = auto()

    # Menu: Detect Audio LCL.
    DETECTING_DEVICE_LCL_ENTER = auto()
    DETECTING_DEVICE_LCL_LEAVE = auto()
    SKIPPING_DEVICE_LCL_LEAVE = auto()

    # Menu: Detect Audio EX1.
    DETECTING_DEVICE_EX1_ENTER = auto()
    DETECTING_DEVICE_EX1_LEAVE = auto()
    DETECTING_DEVICE_EX1_FAILED = auto()
    SKIPPING_DEVICE_EX1_LEAVE = auto()

    # Menu: Detect Audio EX2.
    DETECTING_DEVICE_EX2_ENTER = auto()
    DETECTING_DEVICE_EX2_LEAVE = auto()
    DETECTING_DEVICE_EX2_FAILED = auto()
    SKIPPING_DEVICE_EX2_LEAVE = auto()

    # Menu: Detect storage RC1.
    DETECTING_DEVICE_RC1_ENTER = auto()
    DETECTING_DEVICE_RC1_LEAVE = auto()
    DETECTING_DEVICE_RC1_FAILED = auto()
    SKIPPING_DEVICE_RC1_LEAVE = auto()

    # Menu: Detect storage RC2.
    DETECTING_DEVICE_RC2_ENTER = auto()
    DETECTING_DEVICE_RC2_LEAVE = auto()
    DETECTING_DEVICE_RC2_FAILED = auto()
    SKIPPING_DEVICE_RC2_LEAVE = auto()

    # Menu: Clean storage RC1.
    CLEANING_DEVICE_RC1_ENTER = auto()
    CLEANING_DEVICE_RC1_LEAVE = auto()

    # Menu: Clean storage RC2.
    CLEANING_DEVICE_RC2_ENTER = auto()
    CLEANING_DEVICE_RC2_LEAVE = auto()

    # Menu: Initialise audio.
    INITIALISING_AUDIO_ENTER = auto()
    INITIALISING_AUDIO_LEAVE = auto()

    # Menu: Main.
    STARTING_RECORDING_ENTER = auto()
    STARTING_RECORDING_LEAVE = auto()

    # Menu: System.
    MOUNTING_STORAGE_ENTER = auto()
    MOUNTING_STORAGE_LEAVE = auto()
    DISCONNECTING_STORAGE_ENTER = auto()
    DISCONNECTING_STORAGE_LEAVE = auto()
    FORMATTING_STORAGE_ENTER = auto()
    FORMATTING_STORAGE_LEAVE = auto()
    STOPPING_SYSTEM_ENTER = auto()

    # Menu: OnRecord.
    HELPING_ONRECORD_LEAVE = auto()
    STOPPING_RECORDING_ENTER = auto()
    STOPPING_RECORDING_LEAVE = auto()
    SETTING_CUEPOINT_LEAVE = auto()
    TOGGLING_MUTE_LEAVE = auto()
    SHOWING_STATUS_LEAVE = auto()

    # Menu: Date, Time, Name
    PROCESSING_DIGIT_LEAVE = auto()
    PROCESSING_DIGIT0_LEAVE = auto()
    PROCESSING_DIGIT1_LEAVE = auto()
    PROCESSING_DIGIT2_LEAVE = auto()
    PROCESSING_DIGIT3_LEAVE = auto()
    PROCESSING_DIGIT4_LEAVE = auto()
    PROCESSING_DIGIT5_LEAVE = auto()
    PROCESSING_DIGIT6_LEAVE = auto()
    PROCESSING_DIGIT7_LEAVE = auto()
    PROCESSING_DIGIT8_LEAVE = auto()
    PROCESSING_DIGIT9_LEAVE = auto()
    PROCESSING_DIGIT_OK_LEAVE = auto()
    PROCESSING_DIGIT_BACKSPACE_LEAVE = auto()

    # Menu: Playback
    LEAVING_PLAYBACK_LEAVE = auto()
    SELECTING_PAUSE_LEAVE = auto()
    SELECTING_RESUME_LEAVE = auto()
    JUMPING_CUE_NEXT_LEAVE = auto()
    JUMPING_CUE_PREVIOUS_LEAVE = auto()
    SEEKING_NEXT_LEAVE = auto()
    SEEKING_PREVIOUS_LEAVE = auto()
    HELPING_PLAYBACK_LEAVE = auto()
    JUMPING_CLIP_NEXT_LEAVE = auto()
    JUMPING_CLIP_PREVIOUS_LEAVE = auto()

    # No specific menu.
    RETURNING_TRUE_LEAVE = auto()
    RETURNING_FALSE_LEAVE = auto()
