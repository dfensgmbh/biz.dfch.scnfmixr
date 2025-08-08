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
