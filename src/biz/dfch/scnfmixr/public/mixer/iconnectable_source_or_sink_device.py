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

"""Module iconnectable_source_or_sink_device."""

from __future__ import annotations
from typing import cast, TYPE_CHECKING
from .iconnectable_set import IConnectableSet

if TYPE_CHECKING:
    from .iconnectable_source_device import IConnectableSourceDevice
    from .iconnectable_sink_device import IConnectableSinkDevice


class IConnectableSourceOrSinkDevice(IConnectableSet):
    """Represents a device with connectable source and sink point sets."""

    def as_source(self) -> "IConnectableSourceDevice":
        """Casts the device as a source device.

        Raises:
            TypeError: If the instance is not a `IConnectableSourceDevice`.
        """

        from .iconnectable_source_device import IConnectableSourceDevice\
            # pylint: disable=C0415

        if not isinstance(self, IConnectableSourceDevice):
            raise TypeError

        return cast(IConnectableSourceDevice, self)

    def as_sink(self) -> "IConnectableSinkDevice":
        """Casts the device as a sink device.

        Raises:
            TypeError: If the instance is not a `IConnectableSinkDevice`.
        """

        from .iconnectable_sink_device import IConnectableSinkDevice\
            # pylint: disable=C0415

        if not isinstance(self, IConnectableSinkDevice):
            raise TypeError

        return cast(IConnectableSinkDevice, self)
