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

"""Module iconnectable_source_device."""

from __future__ import annotations

from .iconnectable_source_or_sink_device import IConnectableSourceOrSinkDevice
from .iconnectable_source_point import IConnectableSourcePoint
from .iconnectable_source_set import IConnectableSourceSet


class IConnectableSourceDevice(
        IConnectableSourceSet,
        IConnectableSourceOrSinkDevice):
    """Represents a device with a source point set connectable to a sink signal
    point set."""

    @property
    def sources(self) -> list[IConnectableSourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items
                if isinstance(e, IConnectableSourcePoint)]

    def as_source_set(self) -> IConnectableSourceSet:
        """The associated signal points as an IConnectableSourceSet."""

        from .source_set_view import SourceSetView  # pylint: disable=C0415

        return SourceSetView(self.sources, self)
