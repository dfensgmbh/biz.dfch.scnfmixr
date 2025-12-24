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

"""Module UiEventInfo"""

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class UiEventInfo:
    """Audio information for state and transition enter and leave events.

    Attributes:
        name (StrEnum | None): The language independent name of the audio
            information.
        is_loop (bool): True, if the audio should be looped; false otherwise.
    """
    name: StrEnum | None
    is_loop: bool
