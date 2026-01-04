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

"""Texts for DE transition event messages."""

# noqa: E501
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventDe: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
guid:eb686a85-3827-4f71-86d6-c7c3ca70c65f
""",

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
guid:521f357c-58ad-4b43-b9d8-bd983cfc8def
""",

    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
guid:5caf2b51-a921-4c2f-95e9-43fc75a74590
""",

    # Menu: Detect HID HI2.
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
guid:beb5c507-6a5f-4520-a5f3-20c056ed3d59
""",

    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
guid:ce598696-3994-4966-9016-a17dd934c378
""",

    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
guid:adefaa59-069b-4987-9074-640733cd2dcb
""",

    # Menu: Detect HID HI3.

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
guid:b1f37144-ba69-49e6-a0cc-dd7e15769d30
""",

    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
guid:54363a35-235c-4c1d-ae74-0d796ddbbd61
""",

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
guid:6ff5555c-410d-459f-8392-d6da70955592
""",

    # Menu: Detect Audio LCL.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
guid:902be5b8-cde4-4e89-b2d1-a531b70bed4e
""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
guid:a2ff549b-b12c-4fe7-8f46-0500f3689327
""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
guid:58411c9d-5876-4242-9862-9e10e3ad4846
""",

    # Menu: Detect Audio EX1.

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
guid:1508eb35-007c-4bb7-9f5a-40c6fdc96f9a
""",

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
guid:a122c1e6-48de-46eb-b1fb-0805a02e77b0
""",

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
guid:ec999b2f-2c5e-490d-a689-e0a2ec5c0568
""",

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
guid:b812a5a6-8d11-4191-b801-908679354ba3
""",

    # Menu: Detect Audio EX2.

    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
guid:46aa3aef-34ad-4506-a9cc-a358f33d61f3
""",

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
guid:0cd3c8ba-720b-499f-9428-d38852345134
""",

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
guid:16a79ca7-016b-42a8-84b0-3e411c776698
""",

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
guid:f872de98-5d10-477a-af5c-7e36b2f9a18a
""",

    # Menu: Detect storage RC1.

    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
guid:c4f3d141-6ba8-4c89-8788-edb496f4f4a5
""",

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
guid:c07e7f10-fec4-4f5a-be1f-4a6cbd4ede87
""",

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
guid:b8a21383-b68c-4884-9ad8-31d2c5a33f60
""",

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
guid:b59e03ef-d96f-4da6-92fb-e31e949f6e8a
""",

    # Menu: Detect storage RC2.

    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
guid:a351ad59-2306-4a28-80b8-2f06dc1ed806
""",

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
guid:7db0153b-968d-485c-ba27-a87fc7347f7d
""",

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
guid:c5cd1291-cad2-4d3f-ac76-5b66cbd59a85
""",

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
guid:ddd3bc6e-f60c-46df-b9d1-81e45bc9761c
""",

    # Menu: Clean storage RC1.

    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
guid:0eb65e0e-acb8-493b-b391-67f1bf48cb93
""",

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
guid:a848f0b6-3a81-489c-af98-068c25781015
""",

    # Menu: Clean storage RC2.

    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
guid:d2896326-bd8f-4755-a297-92ba458e9e66
""",

    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
guid:ce9e7a9a-e6b5-4906-8af2-fe6b8e04908c
""",

    # Menu: Initialise audio.

    TransitionEvent.INITIALISING_AUDIO_ENTER: """
guid:21f72f0d-46fb-4c3b-9aa6-bb73e846771e
""",

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
guid:19921372-bcfe-4dd0-92a7-f881da22b36c
""",

    # Menu: Main.

    TransitionEvent.STARTING_RECORDING_ENTER: """
guid:f63f98b0-b7f5-4aed-ae64-7d7c90443026
""",

    TransitionEvent.STARTING_RECORDING_LEAVE: """
guid:2010bcb1-b347-40d3-b83e-fafed2b9fcb9
""",

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
guid:798f31ee-867d-46db-86ef-363f9499c7aa
""",

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
guid:e269d4a9-0fff-4dd4-8a0f-27a933d34b82
""",

    # Menu: System.

    TransitionEvent.MOUNTING_STORAGE_ENTER: """
guid:e3129704-3385-4f3d-959c-39f8f2a8ceb4
""",

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
guid:dea10229-e9d7-4919-87cf-60c28703b44a
""",

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
guid:dc266b53-96f9-4928-b4cd-9604b1ee6853
""",

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
guid:1bc3de7f-2fea-42f7-8716-aa7bf9e27c5a
""",

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
guid:35fe59ce-12b0-434d-aaa8-30ec962323f7
""",

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
guid:7746cdfa-9c89-4b50-86d1-78221f69d136
""",

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
guid:7bf38858-c1db-4dc6-97dd-5be690c07e41
""",

    # Menu: OnRecord.

    TransitionEvent.HELPING_ONRECORD_LEAVE: """
guid:48b0b1e0-b05d-41dc-99af-20964612b1e8
""",

    TransitionEvent.STOPPING_RECORDING_ENTER: """
guid:b8ba29a3-b93c-4617-a350-c507baca5bfb
""",

    TransitionEvent.STOPPING_RECORDING_LEAVE: """
guid:c5db16b3-b523-40ce-980a-772ae65c99ec
""",

    # No audio menu necessary.
    TransitionEvent.SETTING_CUEPOINT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.TOGGLING_MUTE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SHOWING_STATUS_LEAVE: """""",

    # Menu: Date, Time, Name

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """""",

    # Menu: Playback

    # No audio menu necessary.
    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SELECTING_PAUSE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SELECTING_RESUME_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SEEKING_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.HELPING_PLAYBACK_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """""",

    # No specific menu.

    # No audio menu necessary.
    TransitionEvent.RETURNING_TRUE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.RETURNING_FALSE_LEAVE: """""",
}
