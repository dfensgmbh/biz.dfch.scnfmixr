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

# noqa: E501
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventIt: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
guid:c22a6b69-a3bb-4a5e-b4ab-f8c2ff76b6b2""",

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
guid:fc15d0b5-5bb3-4b95-8841-df13b624e0da""",

    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
guid:dd2a0b0f-c941-4525-a8c7-7fd2fc02eefa
""",

    # Menu: Detect HID HI2.
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
guid:0da84985-9f90-4687-868e-0b70ea782c62
""",

    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
guid:a07f51c8-1c34-4398-962a-389428499758
""",

    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
guid:fde8c58c-cf5c-4688-b2ca-c52d9fa34622
""",


    # Menu: Detect HID HI3.

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
guid:39ee9fc0-26c8-4329-b88f-59b772a23709
""",

    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
guid:4dc5e677-2164-4a76-8679-b31d4749537e
""",

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
guid:d787aa93-0ebf-4b8d-963e-49c32f3fc6a7
""",

    # Menu: Detect Audio LCL.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
guid:f608c615-75f8-4c69-895f-01c4915854de
""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
guid:6ec8e1d4-bf88-4ce0-adfd-b9f1f7938835
""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
guid:a81f8c16-7d3e-481a-82b9-0cee7b549c5f
""",

    # Menu: Detect Audio EX1.

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
guid:9c5da6ff-1f41-42a9-9148-8a63ed5a3470
""",

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
guid:0aec60bb-5f6f-4e79-952c-72e9e6876b4e
""",

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
guid:b8fb48eb-d602-419f-9aaf-2cbe432b6793
""",

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
guid:7ff0bc16-6434-4cfb-871a-2245f3a57c91
""",

    # Menu: Detect Audio EX2.

    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
guid:7954c384-3f73-4f08-b2ff-5c931ec4cc59
""",

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
guid:db8f75d9-75cb-427b-a699-f9321260bc64
""",

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
guid:6c9f28cb-443e-4f37-809a-5ce7ab767128
""",

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
guid:e82fd497-2a96-4dc4-a7a4-d2b51e18dd51
""",

    # Menu: Detect storage RC1.

    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
guid:5c808c58-e6b5-40d9-a761-0c73a91de932
""",

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
guid:8296e969-fc8d-45bd-ae9d-091b59564474
""",

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
guid:7677aa91-a066-475c-959f-8ad319ac4512
""",

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
guid:6dbe0bf2-b747-4ca8-a877-758d60923bb4
""",

    # Menu: Detect storage RC2.
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
guid:401f4b99-f540-4493-9fb2-8b46c7bafe54
""",

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
guid:9afa9dfb-f6ee-4c3e-9101-4c037feefbe1
""",

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
guid:9b566a4c-12e6-46a1-9dbe-4312c773bfad
""",

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
guid:decde18d-8a66-485f-a657-a16dcf96ab90
""",

    # Menu: Clean storage RC1.
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
guid:415da073-1c60-435e-a4d0-2a1efb682de0
""",

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
guid:20c2b945-4caf-49af-bfc2-36f62b81597c
""",

    # Menu: Clean storage RC2.
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
guid:3280d525-f2cb-480b-b2e1-d98ef5e603d8
""",

    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
guid:980bd868-340a-4d2f-a032-3e1803d2749c
""",

    # Menu: Initialise audio.

    TransitionEvent.INITIALISING_AUDIO_ENTER: """
guid:7dbd64a0-512b-442f-bfe3-c44384cdc4d1
""",

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
guid:0b1c35ed-9f1d-496e-847c-6bff19ddb3d0
""",

    # Menu: Main.

    TransitionEvent.STARTING_RECORDING_ENTER: """
guid:173dc8f9-25cb-4d0d-8c9a-d5b41f0e1f53
""",

    TransitionEvent.STARTING_RECORDING_LEAVE: """
guid:2f571ceb-9097-41e1-b1da-997e4d968577
""",

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
guid:5c962c08-999b-4cd0-bd5b-c98c175f5090
""",

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
guid:62cdb897-6a10-42dd-8353-2922e2d2b26e
""",

    # Menu: System.

    TransitionEvent.MOUNTING_STORAGE_ENTER: """
guid:f37ffd2e-6ca0-4934-a709-e027d8e4d6c2
""",

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
guid:0c500c00-6daf-46fd-87fb-f812f343a3f6
""",

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
guid:3ea75f82-9f69-4f73-82b1-cfa45c11a661
""",

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
guid:068e4ea0-427f-4566-a61c-aa63c6a907d5
""",

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
guid:8843a933-8237-4e98-bda7-1bdc1a11703d
""",

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
guid:161dd5d0-cc2d-4e01-ba0e-2504bbbe44f5
""",

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
guid:f807fda9-d4d6-4308-8946-79bbd5ecbe5c
""",

    # Menu: OnRecord.

    TransitionEvent.HELPING_ONRECORD_LEAVE: """
guid:cd83eed2-cff2-4040-8475-e3665432998b
""",

    TransitionEvent.STOPPING_RECORDING_ENTER: """
guid:2b30cbdf-647d-4cc1-8774-03c2cbd00ea2
""",

    TransitionEvent.STOPPING_RECORDING_LEAVE: """
guid:57fb4216-aeae-4999-b899-2a53346dbe15
""",

    TransitionEvent.SETTING_CUEPOINT_LEAVE: """
guid:87790c31-d850-4a77-9611-7cb89a2c7dce
""",

    TransitionEvent.TOGGLING_MUTE_LEAVE: """
guid:c8c5c89a-ae32-4030-824c-4688d07de3e3
""",

    TransitionEvent.SHOWING_STATUS_LEAVE: """
guid:ae0d8378-7dae-45d1-8b89-4a554e6e0a0b
""",

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
