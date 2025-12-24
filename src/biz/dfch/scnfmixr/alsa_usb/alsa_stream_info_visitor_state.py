# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

from enum import Enum, auto


class AlsaStreamInfoVisitorState(Enum):
    """Describes the different states of the ALSA steram info visitor.

    Attributes:
        DEFAULT: The initial and default state of the visitor.
        PLAYBACK: The state when the `Playback` section has been reached.
        CAPTURE: The state when the `Capture` section has been reached.
        INTERFACE: The state when an `Interface` section has been reached.
    """

    DEFAULT = auto()
    PLAYBACK = auto()
    CAPTURE = auto()
    INTERFACE = auto()
