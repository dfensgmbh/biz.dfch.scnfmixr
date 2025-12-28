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

"""Module sink_set_view."""

from __future__ import annotations
from collections.abc import Iterator

from .connection_policy import ConnectionPolicy
from .iconnectable_point import IConnectablePoint
from .iconnectable_sink_set import IConnectableSinkSet
from .iconnectable_sink_device import IConnectableSinkDevice


class SinkSetView(IConnectableSinkSet):
    """A view to an IConnectableSinkSet."""

    def __init__(
        self,
        items: list[IConnectablePoint],
        device: IConnectableSinkDevice
    ) -> None:

        super().__init__(type(self).__name__)

        assert isinstance(items, list)
        assert isinstance(device, IConnectableSinkDevice)

        self._items = dict.fromkeys(items, None)
        self._device = device

    def __iter__(self) -> Iterator[IConnectablePoint]:
        return iter(list(self._items.keys()))

    def __getitem__(self, index: int) -> IConnectablePoint:
        return list(self._items.keys())[index]

    def acquire(self):
        return self._device.acquire()

    def release(self):
        return self._device.release()

    @property
    def is_source(self):
        return self._device.is_source

    @property
    def is_sink(self):
        return self._device.is_sink

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):
        return self._device.connect_to(other, policy)

    @property
    def is_acquired(self):
        return self._device.is_acquired

    @is_acquired.setter
    def is_acquired(self, value):
        self._device.is_acquired = value
