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

# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventEn: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.

    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Trying to detect input device ONE.
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
<<<sound-intro.wav>>>
""",  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Skipped input device ONE.
""",  # noqa: E501

    # Menu: Detect HID HI2.

    # Menu: Detect HID HI3.

    # Menu: Detect Audio LCL.

    # Menu: Detect Audio EX1.

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Trying to detect external device EX1.
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Successfully detected external device EX1.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
External device detection EX1 failed.

Check cabling and port location.
""",  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Skipped external device EX1.
""",  # noqa: E501

    # Menu: Detect Audio EX2.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Trying to detect external device EX2.
""",  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Successfully detected external device EX2.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
External device detection EX2 failed.

Check cabling and port location.
""",  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Skipped external device EX2.
""",  # noqa: E501

    # Menu: Storage RC1.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Trying to detect storage device RC1.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Successfully detected storage device RC1.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Storage device detection RC1 failed.

Check cabling and port location.
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Skipped storage device RC1.
""",  # noqa: E501

    # OK
    # Menu: Storage RC2.
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Trying to detect storage device RC2.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Successfully detected storage device RC2.
""",  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Storage device detection RC2 failed.

Check cabling and port location.
""",  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Skipped storage device RC2.
""",  # noqa: E501

    # Menu: Initialise audio.

    # Menu: Main.
    # OK
    TransitionEvent.STARTING_RECORDING_ENTER: """
Preparing for recording.
""",  # noqa: E501

    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE: """
Recording started.
""",  # noqa: E501

    # Menu: System.

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
""",  # noqa: E501

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
""",  # noqa: E501


    # Menu: OnRecord.
    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER: """
Stopping recording.

This might take some seconds.
""",  # noqa: E501

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
""",  # noqa: E501

    # Menu: Date, Time, Name

    # Menu: Playback

    # No specific menu.
}
