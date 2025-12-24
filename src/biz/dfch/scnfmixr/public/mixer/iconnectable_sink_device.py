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

"""Module iconnectable_sink_device."""

from __future__ import annotations

from .iconnectable_sink_point import IConnectableSinkPoint
from .iconnectable_sink_set import IConnectableSinkSet
from .iconnectable_source_or_sink_device import IConnectableSourceOrSinkDevice


class IConnectableSinkDevice(
        IConnectableSinkSet,
        IConnectableSourceOrSinkDevice):
    """Represents a device with a sink signal point set connectable to a source
    signal point set."""

    @property
    def sinks(self) -> list[IConnectableSinkPoint]:
        """The associated sink signal points with this device."""

        return [e for e in self._items
                if isinstance(e, IConnectableSinkPoint)]

    def as_sink_set(self) -> IConnectableSinkSet:
        """The associated signal points as an IConnectableSinkSet."""

        from .sink_set_view import SinkSetView  # pylint: disable=C0415

        return SinkSetView(self.sinks, self)
