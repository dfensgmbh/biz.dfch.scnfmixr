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

"""Package signal_point."""

from __future__ import annotations
from abc import abstractmethod

from biz.dfch.scnfmixr.public.mixer import IConnectablePoint
from biz.dfch.scnfmixr.public.mixer import IConnectableSourcePoint
from biz.dfch.scnfmixr.public.mixer import IConnectableSinkPoint
from biz.dfch.scnfmixr.public.mixer import IConnectableSet
from biz.dfch.scnfmixr.public.mixer import IConnectableSourceSet
from biz.dfch.scnfmixr.public.mixer import IConnectableSinkSet

__all__ = [
    "ITerminalSourceOrSinkPoint",
    "ITerminalSourcePoint",
    "ITerminalSinkPoint",
    "IConnectableSourceOrSinkDevice",
    "IConnectableSourceDevice",
    "IConnectableSinkDevice",
    "IConnectableDevice",
    "ITerminalSourceOrSinkDevice",
    "ITerminalSourceDevice",
    "ITerminalSinkDevice",
    "ITerminalDevice",
    "IChannel",
    "IMonoChannel",
    "IStereoChannel",
    "IBusSourceOrSinkPoint",
    "IBusSourcePoint",
    "IBusSinkPoint",
    "IBusDevice",
]


class ITerminalSourceOrSinkPoint(IConnectablePoint):
    """Represents a signal generating point from a device entering the system
    or a signal receiving point to a device leaving the system."""


class ITerminalSourcePoint(IConnectableSourcePoint, ITerminalSourceOrSinkPoint):
    """Represents a signal generating point from a device entering the
    system.

    This is typically an audio source or audio input such as a *microphone* or
    an *audio interface*.
    """


class ITerminalSinkPoint(IConnectableSinkPoint, ITerminalSourceOrSinkPoint):
    """Represents a signal receiving point to a device leaving the system.

    This is typically an audio output such as a *loudspeaker* or an *audio
    interface*.
    """


class IConnectableSourceOrSinkDevice(IConnectableSet):
    """Represents a device with connectable source and sink point sets."""


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


class IConnectableDevice(IConnectableSourceDevice, IConnectableSinkDevice):
    """Represents a device consisting of sources and sinks."""


class ITerminalSourceOrSinkDevice(IConnectableSourceOrSinkDevice):
    """Represents a device consisting of one or more terminal source or sink
    signal points."""

    @property
    @abstractmethod
    def points(self) -> list[ITerminalSourceOrSinkPoint]:
        """The associated signal points with this device."""

        return [e for e in self._items if isinstance(
            e, ITerminalSourceOrSinkPoint)]


class ITerminalSourceDevice(
        IConnectableSourceDevice,
        ITerminalSourceOrSinkDevice):
    """Represents a device consisting of one or more terminal source signal
    points."""


class ITerminalSinkDevice(IConnectableSinkDevice, ITerminalSourceOrSinkDevice):
    """Represents a device consisting of one or more terminal sink signal
    points."""


class ITerminalDevice(
        ITerminalSourceDevice,
        ITerminalSinkDevice,
        IConnectableDevice):
    """Represents a device consisting of one or more terminal source and sink
    points."""

    @property
    def sources(self) -> list[ITerminalSourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items.keys() if isinstance(e, ITerminalSourcePoint)]

    @property
    def sinks(self) -> list[ITerminalSinkPoint]:
        """The associated signal sink points with this device."""

        return [e for e in self._items.keys() if isinstance(e, ITerminalSinkPoint)]


class IChannel(IConnectableSinkDevice):
    """Represents an audio device with a channel strip entering the system."""

    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of signal points in this channel."""

    @property
    def device(self) -> ITerminalSourceDevice:
        """The associate external device with this channel."""

    @property
    def points(self) -> list[ITerminalSourcePoint]:
        """The source signal point of this channel."""

        return [e for e in self._items if isinstance(e, ITerminalSourcePoint)]


class IMonoChannel(IChannel):
    """Represents an audio device with a channel strip entering the system."""

    @property
    def count(self) -> int:
        return 1

    @property
    def mono(self) -> ITerminalSourcePoint:
        """The mono source signal point of this channel."""

        return self.points[0]


class IStereoChannel(IChannel):
    """Represents an audio device with a channel strip entering the system."""

    @property
    def count(self) -> int:
        return 2

    @property
    def left(self) -> ITerminalSourcePoint:
        """The left source signal point of this channel."""

        return self.points[0]

    @property
    def right(self) -> ITerminalSourcePoint:
        """The right source signal point of this channel."""

        return self.points[1]


class IBusSourceOrSinkPoint(IConnectablePoint):
    """Represents a signal point entering or leaving a bus."""


class IBusSourcePoint(IConnectableSourcePoint):
    """Represents signal point leaving a bus.

    This is the bus output.
    """


class IBusSinkPoint(IConnectableSinkPoint):
    """Represents signal point entering a bus.

    This is the bus input.
    """


class IBusDevice(IConnectableDevice):
    """Represents a mix bus.

    A mix bus represents an internaö signal path with a channel strip.

    Attributes:

        channel_count (int): The number of bus channels.
        input (IBusSinkPoint): The bus input.
        output (IBusSourcePoint): The bus output.
    """

    @property
    def channel_count(self) -> int:
        """Returns the number of channels of the bus."""

        assert len(self.input) == len(self.output)

        return len(self.input)

    @property
    def input(self) -> IBusSinkPoint:
        """TThe bus input."""

        return [e for e in self._items if isinstance(e, IBusSinkPoint)]

    @property
    def output(self) -> IBusSourcePoint:
        """The bus output."""

        return [e for e in self._items if isinstance(e, IBusSourcePoint)]
