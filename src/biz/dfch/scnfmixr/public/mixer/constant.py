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

"""Package constant."""

from enum import StrEnum


class Constant(StrEnum):
    """Mixer port constants."""

    JACK_ALSA_PREFIX = "Alsa"
    JACK_MIXBUS_PREFIX = "Mixbus"
    JACK_SEPARATOR = ":"
    JACK_INFIX = "-"
    JACK_INPUT = "I"
    JACK_OUTPUT = "O"
    JACK_SOURCE_PORT_INFIX_BASE = "capture_"
    JACK_SINK_PORT_INFIX_BASE = "playback_"
