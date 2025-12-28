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

"""Texts for IT transition event messages."""

# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventIt: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
""",  # noqa: E501

    # Menu: Detect HID HI2.
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
""",  # noqa: E501


    # Menu: Detect HID HI3.
    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
""",  # noqa: E501

    # Menu: Detect Audio LCL.
    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
""",  # noqa: E501

    # Menu: Detect Audio EX1.
    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
""",  # noqa: E501

    # Menu: Detect Audio EX2.
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
""",  # noqa: E501

    # Menu: Detect storage RC1.
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
""",  # noqa: E501

    # Menu: Detect storage RC2.
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
""",  # noqa: E501

    # Menu: Clean storage RC1.
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
""",  # noqa: E501

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
""",  # noqa: E501

    # Menu: Clean storage RC2.
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
""",  # noqa: E501

    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
""",  # noqa: E501

    # Menu: Initialise audio.
    TransitionEvent.INITIALISING_AUDIO_ENTER: """
""",  # noqa: E501

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
""",  # noqa: E501

    # Menu: Main.
    TransitionEvent.STARTING_RECORDING_ENTER: """
""",  # noqa: E501

    TransitionEvent.STARTING_RECORDING_LEAVE: """
""",  # noqa: E501

    # Menu: System.
    TransitionEvent.MOUNTING_STORAGE_ENTER: """
""",  # noqa: E501

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
""",  # noqa: E501

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
""",  # noqa: E501

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
""",  # noqa: E501

    # Menu: OnRecord.
    TransitionEvent.HELPING_ONRECORD_LEAVE: """
""",  # noqa: E501

    TransitionEvent.STOPPING_RECORDING_ENTER: """
""",  # noqa: E501

    TransitionEvent.STOPPING_RECORDING_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SETTING_CUEPOINT_LEAVE: """
""",  # noqa: E501

    TransitionEvent.TOGGLING_MUTE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SHOWING_STATUS_LEAVE: """
""",  # noqa: E501

    # Menu: Date, Time, Name
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """
""",  # noqa: E501

    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """
""",  # noqa: E501

    # Menu: Playback
    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SELECTING_PAUSE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SELECTING_RESUME_LEAVE: """
""",  # noqa: E501

    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """
""",  # noqa: E501

    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SEEKING_NEXT_LEAVE: """
""",  # noqa: E501

    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """
""",  # noqa: E501

    TransitionEvent.HELPING_PLAYBACK_LEAVE: """
""",  # noqa: E501

    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """
""",  # noqa: E501

    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """
""",  # noqa: E501

    # No specific menu.
    TransitionEvent.RETURNING_TRUE_LEAVE: """
""",  # noqa: E501

    TransitionEvent.RETURNING_FALSE_LEAVE: """
""",  # noqa: E501
}
