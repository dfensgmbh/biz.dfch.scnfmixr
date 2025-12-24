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

"""Module state_event."""

from enum import StrEnum, auto


class StateEvent(StrEnum):
    """State Enter and Leave audio information."""

    # Detection of local audio device.
    INITIALISE_LCL_ENTER = auto()
    # This will be the welcome sound.
    INITIALISE_LCL_LEAVE = auto()

    # Detection of input device.
    INITIALISE_HI1_ENTER = auto()
    # This will be the welcome sound.
    INITIALISE_HI1_LEAVE = auto()

    SELECT_LANGUAGE_ENTER = auto()

    INITIALISE_EX1_ENTER = auto()
    INITIALISE_EX2_ENTER = auto()

    INITIALISE_RC1_ENTER = auto()
    INITIALISE_RC2_ENTER = auto()

    SET_DATE_ENTER = auto()
    SET_TIME_ENTER = auto()
    SET_NAME_ENTER = auto()

    INIT_AUDIO_LEAVE = auto()

    MAIN_ENTER = auto()

    SYSTEM_ENTER = auto()

    STORAGE_MANAGEMENT_ENTER = auto()

    # No specific menu.
    SWALLOW_STATE_ENTER_LEAVE = auto()
