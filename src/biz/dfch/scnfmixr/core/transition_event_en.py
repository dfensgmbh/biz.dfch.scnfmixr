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

"""Module transition_event_en."""

from .transition_event import TransitionEvent


class TransitionEventEn(dict[TransitionEvent, str]):
    """Texts for EN transition event messages."""

    # Menu: Detect HID HI1.

    #OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER = """
Trying to detect input device ONE.
"""  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE = """
<<<sound-intro.wav>>>
"""  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE = """
Skipped input device ONE.
"""  # noqa: E501

    # Menu: Detect HID HI2.

    # Menu: Detect HID HI3.

    # Menu: Detect Audio LCL.

    # Menu: Detect Audio EX1.

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_ENTER = """
Trying to detect external device EX1.
"""  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE = """
Successfully detected external device EX1.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED = """
External device detection EX1 failed.

Check cabling and port location.
"""  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE = """
Skipped external device EX1.
"""  # noqa: E501

    # Menu: Detect Audio EX2.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER = """
Trying to detect external device EX2.
"""  # noqa: E501

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE = """
Successfully detected external device EX2.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED = """
External device detection EX2 failed.

Check cabling and port location.
"""  # noqa: E501

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE = """
Skipped external device EX2.
"""  # noqa: E501

    # Menu: Storage RC1.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER = """
Trying to detect storage device RC1.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE = """
Successfully detected storage device RC1.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED = """
Storage device detection RC1 failed.

Check cabling and port location.
"""  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE = """
Skipped storage device RC1.
"""  # noqa: E501

    # OK
    # Menu: Storage RC2.
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER = """
Trying to detect storage device RC2.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE = """
Successfully detected storage device RC2.
"""  # noqa: E501

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED = """
Storage device detection RC2 failed.

Check cabling and port location.
"""  # noqa: E501

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE = """
Skipped storage device RC2.
"""  # noqa: E501

    # Menu: Initialise audio.

    # Menu: Main.
    # OK
    TransitionEvent.STARTING_RECORDING_ENTER = """
Preparing for recording.
"""  # noqa: E501

    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE = """
Recording started.
"""  # noqa: E501

    # Menu: System.

    # Menu: OnRecord.
    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER = """
Stopping recording.

This might take some seconds.
"""  # noqa: E501

    # OK
    TransitionEvent.STOPPING_RECORDING_LEAVE = """
Recording stopped.

You can now go to the playback menu and listen to the recording or delete the recording.
"""  # noqa: E501

    # OK
    TransitionEvent.HELPING_ONRECORD_LEAVE = """
The "Recording" menu.

Press "1" to stop recording.
Press "2" to set a cue marker.
Press "3" to mute the local device for the recording.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # Menu: Date, Time, Name

    # Menu: Playback

    # No specific menu.
