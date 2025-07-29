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
