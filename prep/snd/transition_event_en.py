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

"""Texts for EN transition event messages."""

# noqa: E501  # NOSONAR  python:S125
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventEn: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.

    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Trying to detect input device ONE.
""",

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
<<<sound-intro.wav>>>
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Skipped input device ONE.
""",

    # Menu: Detect HID HI2.

    # DFTODO: No audio menu.
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Trying to detect input device TWO.
""",

    # DFTODO: No audio menu.
    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Skipped input device TWO.
""",

    # Menu: Detect HID HI3.

    # DFTODO: No audio menu.
    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Trying to detect input device THREE.
""",

    # DFTODO: No audio menu.
    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Skipped input device THREE.
""",

    # Menu: Detect Audio LCL.

    # OK. No audio menu necessary.
    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """""",

    # Menu: Detect Audio EX1.

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Trying to detect external device EX1.
""",

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Successfully detected external device EX1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
External device detection EX1 failed.

Check cabling and port location.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Skipped external device EX1.
""",

    # Menu: Detect Audio EX2.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Trying to detect external device EX2.
""",

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Successfully detected external device EX2.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
External device detection EX2 failed.

Check cabling and port location.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Skipped external device EX2.
""",

    # Menu: Storage RC1.

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Trying to detect storage device RC1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Successfully detected storage device RC1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Storage device detection RC1 failed.

Check cabling and port location.
""",

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Skipped storage device RC1.
""",

    # OK
    # Menu: Storage RC2.
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Trying to detect storage device RC2.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Successfully detected storage device RC2.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Storage device detection RC2 failed.

Check cabling and port location.
""",

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Skipped storage device RC2.
""",

    # Menu: Initialise audio.

    # Menu: Main.
    # OK
    TransitionEvent.STARTING_RECORDING_ENTER: """
Preparing for recording.
""",

    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE: """
Recording started.
""",

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
Trying to delete last recording.
""",

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
Trying to delete last recording succeeded.
""",

    # Menu: System.

    # DFTODO: No audio menu.
    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Trying to format storage device.
All data on this storage device will be deleted.
""",

    # DFTODO: No audio menu.
    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Trying to format storage device succeeded.
""",


    # Menu: OnRecord.
    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER: """
Stopping recording.

This might take some seconds.
""",

    # OK
    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Recording stopped.

You can now go to the playback menu and listen to the recording or delete the recording.
""",  # noqa: E501

    # OK
    TransitionEvent.HELPING_ONRECORD_LEAVE: """
The "Recording" menu.

Press "1" to stop recording.
Press "2" to set a cue marker.
Press "3" to mute the local device for the recording.
Press "STAR" to repeat this message.
""",

    # Menu: Date, Time, Name

    # Menu: Playback

    # No specific menu.

    # DFTODO: No audio menu.
    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
<<<sound-intro.wav>>>
""",

    # DFTODO: No audio menu.
    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
<<<sound-intro.wav>>>
""",

    # OK. No audio menu necessary.
    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """""",

    # DFTODO: No audio menu.
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Trying to clean recordings from storage device RC1.
""",

    # DFTODO: No audio menu.
    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Trying to clean recordings from storage device RC1 succeeded.
""",

    # DFTODO: No audio menu.
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Trying to clean recordings from storage device RC2.
""",

    # DFTODO: No audio menu.
    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Trying to clean recordings from storage device RC2 succeeded.
""",

    # OK. No audio menu necessary.
    TransitionEvent.INITIALISING_AUDIO_ENTER: """""",

    # OK. No audio menu necessary.
    TransitionEvent.INITIALISING_AUDIO_LEAVE: """""",

    # DFTODO: No audio menu.
    TransitionEvent.MOUNTING_STORAGE_ENTER: """
Trying to mount storage device RC1.
""",

    # DFTODO: No audio menu.
    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
Trying to mount storage device RC1 succeeded.
""",

    # DFTODO: No audio menu.
    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Trying to mount storage device RC2.
""",

    # DFTODO: No audio menu.
    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Trying to mount storage device RC2 succeeded.
""",

    # OK. No audio menu necessary.
    TransitionEvent.STOPPING_SYSTEM_ENTER: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SETTING_CUEPOINT_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.TOGGLING_MUTE_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SHOWING_STATUS_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SELECTING_PAUSE_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SELECTING_RESUME_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SEEKING_NEXT_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.HELPING_PLAYBACK_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.RETURNING_TRUE_LEAVE: """""",

    # OK. No audio menu necessary.
    TransitionEvent.RETURNING_FALSE_LEAVE: """""",
}
