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

"""Module state_event_de."""

from .state_event import StateEvent


class StateEventEn(dict[StateEvent, str]):
    """Texts for EN state events messages."""

    # OK
    StateEvent.INITIALISE_LCL_ENTER = """
The "Initialise Local Device" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.INITIALISE_HI1_ENTER = """
The "Initialise Input Device One" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SELECT_LANGUAGE_ENTER = """
The "Language Selection" menu

Press "1" for english.
Drücken Sie "2" für deutsch.
Selectionner "3" pour français.
Scegliere "4" por italiano.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.INITIALISE_EX1_ENTER = """
The "Initialise External Device One" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.INITIALISE_EX2_ENTER = """
The "Initialise External Device Two" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.INITIALISE_RC1_ENTER = """
The "Initialise Storage Device One" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "6" to format the device.
Press "7" to mount the device.
Press "8" to unmount the device.
Press "9" to clean the device.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.INITIALISE_RC2_ENTER = """
The "Initialise Storage Device Two" menu

Press "1" for device detection.
Press "2" to skip device detection.
Press "6" to format the device.
Press "7" to mount the device.
Press "8" to unmount the device.
Press "9" to clean the device.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SET_DATE_ENTER = """
The "Date" menu

Enter an 8 digit date starting with the 4 digit year, followed by a 2 digit month and a 2 digit day.

To delete a digit, press the "BACK-SPACE" key.
When you are finished entering the value, or to start from the start again, press the "ENTER" key.

Example:

one-nine-two-seven

zero-three-two-seven for the 27th of March in 19 27.

Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SET_TIME_ENTER = """
The "Time" menu

Enter a 4 digit time starting with the 2 digit 24 hours, followed by the 2 digit minutes.

To delete a digit, press the "BACK-SPACE" key.
When you are finished entering the value, or to start from the start again, press the "ENTER" key.

Example:

one-four-zero-three for 3 minutes after 2 o'clock in the afternoon.

Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SET_NAME_ENTER = """
The "Name" menu

Enter an 8 digit name used as the unique name in your recording.

To delete a digit, press the "BACK-SPACE" key.
When you are finished entering the value, or to start from the start again, press the "ENTER" key.

Example:

zero-eight-one-five

five-six-four-two for zero-eight 15 56 42.

Press "STAR" to repeat this message.
"""  # noqa: E501

    StateEvent.MAIN_ENTER = """
The "Main" menu

Press "1" to start a stereo recording.
Press "2" to start a dry iso and a stereo recording.
Press "3" to start a wet iso, dry iso and stereo recording.
Press "4" to start playback.
Press "5" to go to the "System" menu.
Press "6" to set a new name for your recording.
Press "9" to stop the device.
Press "STAR" to repeat this message.
"""  # noqa: E501

    StateEvent.SYSTEM_ENTER = """
The "System" menu

Press "1" to go to the "Main" menu.
Press "2" to select the language.
Press "3" to go to the "Storage" menu.
Press "4" to set the date.
Press "5" to set the time.
Press "9" to stop the device.

Press "STAR" to repeat this message.
"""  # noqa: E501

        # # HELP = InputEventMap.KEY_ASTERISK
        # # SELECT_MAIN = InputEventMap.KEY_1
        # # SELECT_LANGUAGE = InputEventMap.KEY_2
        # SELECT_STORAGE = InputEventMap.KEY_3
        # # SET_DATE = InputEventMap.KEY_4
        # # SET_TIME = InputEventMap.KEY_5
        # SET_NAME = InputEventMap.KEY_6
        # DETECT_STORAGE = InputEventMap.KEY_7
        # DISCONNECT_STORAGE = InputEventMap.KEY_8
        # STOP_SYSTEM = InputEventMap.KEY_9