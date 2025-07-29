# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
