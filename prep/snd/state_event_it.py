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

"""Texts for IT state event messages."""

# cSpell:disable

from biz.dfch.scnfmixr.core.state_event import StateEvent


StateEventIt: dict[StateEvent, str] = {

    # Detection of local audio device.
    StateEvent.INITIALISE_LCL_ENTER: """
""",  # noqa: E501

    # This will be the welcome sound.
    StateEvent.INITIALISE_LCL_LEAVE: """
""",  # noqa: E501

    # Detection of input device.
    StateEvent.INITIALISE_HI1_ENTER: """
""",  # noqa: E501

    # This will be the welcome sound.
    StateEvent.INITIALISE_HI1_LEAVE: """
""",  # noqa: E501

    StateEvent.SELECT_LANGUAGE_ENTER: """
""",  # noqa: E501

    StateEvent.INITIALISE_EX1_ENTER: """
""",  # noqa: E501

    StateEvent.INITIALISE_EX2_ENTER: """
""",  # noqa: E501

    StateEvent.INITIALISE_RC1_ENTER: """
""",  # noqa: E501

    StateEvent.INITIALISE_RC2_ENTER: """
""",  # noqa: E501

    StateEvent.SET_DATE_ENTER: """
""",  # noqa: E501

    StateEvent.SET_TIME_ENTER: """
""",  # noqa: E501

    StateEvent.SET_NAME_ENTER: """
""",  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE: """
""",  # noqa: E501

    StateEvent.MAIN_ENTER: """
""",  # noqa: E501

    StateEvent.SYSTEM_ENTER: """
""",  # noqa: E501

    StateEvent.STORAGE_MANAGEMENT_ENTER: """
""",  # noqa: E501

    # No specific menu.
    StateEvent.SWALLOW_STATE_ENTER_LEAVE: """
""",  # noqa: E501
}
