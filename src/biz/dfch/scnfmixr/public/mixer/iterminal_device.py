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

"""Module iterminal_device."""

from __future__ import annotations

from .iterminal_source_point import ITerminalSourcePoint
from .iterminal_sink_point import ITerminalSinkPoint
from .iconnectable_device import IConnectableDevice
from .iterminal_sink_device import ITerminalSinkDevice
from .iterminal_source_device import ITerminalSourceDevice


class ITerminalDevice(
        ITerminalSourceDevice,
        ITerminalSinkDevice,
        IConnectableDevice):
    """Represents a device consisting of one or more terminal source and sink
    points."""

    @property
    def sources(self) -> list[ITerminalSourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items.keys()  # pylint: disable=C0201
                if isinstance(e, ITerminalSourcePoint)]

    @property
    def sinks(self) -> list[ITerminalSinkPoint]:
        """The associated signal sink points with this device."""

        return [e for e in self._items.keys()  # pylint: disable=C0201
                if isinstance(e, ITerminalSinkPoint)]
