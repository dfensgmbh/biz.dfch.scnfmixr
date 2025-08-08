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
