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

"""Module iterminal_sink_point."""

from .iconnectable_sink_point import IConnectableSinkPoint
from .iterminal_source_or_sink_point import ITerminalSourceOrSinkPoint


class ITerminalSinkPoint(IConnectableSinkPoint, ITerminalSourceOrSinkPoint):
    """Represents a signal receiving point to a device leaving the system.

    This is typically an audio output such as a *loudspeaker* or an *audio
    interface*.
    """
