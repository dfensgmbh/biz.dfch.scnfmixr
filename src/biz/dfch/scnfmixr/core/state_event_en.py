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

"""Module state_event_en."""

from .state_event import StateEvent


class StateEventEn(dict[StateEvent, str]):
    """Texts for EN state event messages."""

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
Wählen Sie "2" für deutsch.
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
When you are finished entering the value, or to start from the start again, press the "ENTER" or "RETURN" key.

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
When you are finished entering the value, or to start from the start again, press the "ENTER" or "RETURN" key.

Example:

one-four-zero-three for 3 minutes after 2 o'clock in the afternoon.

Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SET_NAME_ENTER = """
The "Name" menu

Enter an 8 digit name used as the unique name in your recording.

To delete a digit, press the "BACK-SPACE" key.
When you are finished entering the value, or to start from the start again, press the "ENTER" or "RETURN" key.

Example:

zero-eight-one-five

five-six-four-two for zero-eight 15 56 42.

Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.MAIN_ENTER = """
The "Main" menu

Press "1" to start a stereo recording.
Press "2" to start a dry iso and a stereo recording.
Press "3" to start a wet iso, dry iso and stereo recording.
Press "4" to start playback.
Press "5" to go to the "System" menu.
Press "6" to set a new name for your next recording.
Press "7" to delete the last recording.
Press "9" to stop the device.
Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.SYSTEM_ENTER = """
The "System" menu

Press "1" to go to the "Main" menu.
Press "2" to select the language.
Press "3" to go to the "Storage" menu.
Press "4" to set the date.
Press "6" to set the time.
Press "9" to stop the device.

Press "STAR" to repeat this message.
"""  # noqa: E501

    # OK
    StateEvent.STORAGE_MANAGEMENT_ENTER = """
The "Storage" menu

Press "0" to disconnect all storage devices.
Press "1" to detect "Storage Device One".
Press "3" to detect "Storage Device Two".
Press "4" to format "Storage Device One".
Press "5" to go to the "System" menu.
Press "6" to format "Storage Device Two".
Press "7" to clean "Storage Device One".
Press "9" to clean "Storage Device Two".

Press "STAR" to repeat this message.
"""  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE = """
Audio system fully initialised.
"""  # noqa: E501
