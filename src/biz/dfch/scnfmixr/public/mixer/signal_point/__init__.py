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
from abc import ABC, abstractmethod
from dataclasses import dataclass


__all__ = [
    "ISignalPath",
    "IConnectablePointOrSet",
    "IConnectablePoint",
    "IConnectableSourcePoint",
    "IConnectableSinkPoint",
    "IConnectableSet",
    "IConnectableSourceSet",
    "IConnectableSinkSet",
    "ISourceOrSinkPoint",
    "ISourcePoint",
    "ISinkPoint",
    "ITerminalSourceOrSinkPoint",
    "ITerminalSourcePoint",
    "ITerminalSinkPoint",
    "ISourceOrSinkDevice",
    "ISourceDevice",
    "ISinkDevice",
    "IDevice",
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


@dataclass(frozen=True)
class ISignalPath(ABC):
    """Represents a signal path from a source signal point to sink signal
    point.

    Attributes:
        name (str): The name of the signal path.
        source (IConnectableSourcePoint): One side of the signal path.
        sink (IConnectableSinkPoint): The other side of the signal path.
    """

    name: str
    source: IConnectableSourcePoint
    sink: IConnectableSinkPoint

    def __init__(
            self,
            source: IConnectableSourcePoint,
            sink: IConnectableSinkPoint
    ):
        """Creates a connection between a connectable source and sink point."""

        super().__init__()

        # assert isinstance(source, IConnectableSourcePoint)
        # assert isinstance(sink, IConnectableSinkPoint)
        assert source.is_point
        assert sink.is_sink

        object.__setattr__(self, "name", f"'{source.name}' +-- '{sink.name}'")
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "sink", sink)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """Determines whether the signal path is active."""

    @abstractmethod
    def remove(self) -> bool:
        """Removes the signal path."""


class IConnectablePointOrSet(ABC):
    """Represents a connectable signal point or signal set."""

    name: str

    def __init__(self, name: str):
        super().__init__()

        assert isinstance(name, str) and name.strip()

        self.name = name

    @property
    @abstractmethod
    def is_source(self) -> bool:
        """Determines whether the object is a source or not."""

    @property
    @abstractmethod
    def is_sink(self) -> bool:
        """Determines whether the object is a sink or not."""

    @property
    @abstractmethod
    def is_point(self) -> bool:
        """Determines whether the object is a point or not."""

    @property
    @abstractmethod
    def is_set(self) -> bool:
        """Determines whether the object is a set or not."""

    @abstractmethod
    def connect_to(self, other: IConnectablePointOrSet) -> set[ISignalPath]:
        """Connect this point set to the other."""

        assert isinstance(other, IConnectablePointOrSet)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class IConnectablePoint(IConnectablePointOrSet):
    """Represents a connectable signal point."""

    @property
    def is_point(self) -> bool:
        return True

    @property
    def is_set(self) -> bool:
        return False

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """Determines whether the signal point is active."""

    def connect(self, other: IConnectablePoint) -> ISignalPath:
        """Connects this point to the other."""

        assert isinstance(other, IConnectablePoint)

        return self.connect_to(other)[0]


class IConnectableSource(IConnectablePointOrSet):
    """IConnectableSourcePointOrSet"""

    @property
    def is_source(self) -> bool:
        return True

    @property
    def is_sink(self) -> bool:
        return False


class IConnectableSink(IConnectablePointOrSet):
    """IConnectableSinkPointOrSet"""

    @property
    def is_source(self) -> bool:
        return False

    @property
    def is_sink(self) -> bool:
        return True


class IConnectableSourcePoint(IConnectablePoint, IConnectableSource):
    """Represents a source point connectable to a sink point."""


class IConnectableSinkPoint(IConnectablePoint, IConnectableSink):
    """Represents a sink point connectable to a source point."""


class IConnectableSet(IConnectablePointOrSet):
    """Represents a connectable signal point set."""

    _items: list[IConnectablePoint]

    def __init__(self, name: str):
        super().__init__(name)

        self._items = []

    @property
    def is_point(self) -> bool:
        return False

    @property
    def is_set(self) -> bool:
        return True

    @property
    @abstractmethod
    def points(self) -> list[IConnectablePoint]:
        """The associated signal points with this device."""

        return self._items


class IConnectableSourceSet(IConnectableSet, IConnectableSource):
    """Represents a source signal point set connectable to a sink point set."""


class IConnectableSinkSet(IConnectableSet, IConnectableSink):
    """Represents a sink signal point set connectable to a source point set."""


class ISourceOrSinkPoint(IConnectablePoint):
    """Represents a signal point."""


class ISourcePoint(IConnectableSourcePoint):
    """Represents a signal generating point."""


class ISinkPoint(IConnectableSinkPoint):
    """Represents a signal receiving point."""


class ITerminalSourceOrSinkPoint(ISourceOrSinkPoint):
    """Represents a signal generating point from a device entering the system
    or a signal receiving point to a device leaving the system."""


class ITerminalSourcePoint(ISourcePoint, ITerminalSourceOrSinkPoint):
    """Represents a signal generating point from a device entering the
    system.

    This is typically an audio source or audio input such as a *microphone* or
    an *audio interface*.
    """


class ITerminalSinkPoint(ISinkPoint, ITerminalSourceOrSinkPoint):
    """Represents a signal receiving point to a device leaving the system.

    This is typically an audio output such as a *loudspeaker* or an *audio
    interface*.
    """


class ISourceOrSinkDevice(IConnectableSet):
    """Represents a device with connectable source and sink point sets."""

    _items: list[IConnectablePoint]

    def __init__(self, name: str):
        super().__init__(name)

        self._items = []

    @property
    @abstractmethod
    def points(self) -> list[IConnectablePoint]:
        """The associated signal points with this device."""

        return self._items


class ISourceDevice(IConnectableSourceSet, ISourceOrSinkDevice):
    """Represents a device with a source point set connectable to a sink signal
    point set."""

    @property
    def points(self) -> list[ISourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items if isinstance(e, ISourcePoint)]


class ISinkDevice(IConnectableSinkSet, ISourceOrSinkDevice):
    """Represents a device with a sink signal point set connectable to a source
    signal point set."""

    @property
    def points(self) -> list[ISinkPoint]:
        """The associated sink signal points with this device."""

        return [e for e in self._items if isinstance(e, ISinkPoint)]


class IDevice(ISourceDevice, ISinkDevice):
    """Represents a device consisting of sources and sinks."""

    @property
    @abstractmethod
    def sources(self) -> list[ISourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items if isinstance(e, ISourcePoint)]

    @property
    @abstractmethod
    def sinks(self) -> list[ISinkPoint]:
        """The associated sink signal points with this device."""

        return [e for e in self._items if isinstance(e, ISinkPoint)]


class ITerminalSourceOrSinkDevice(ISourceOrSinkDevice):
    """Represents a device consisting of one or more terminal source or sink
    signal points."""

    @property
    @abstractmethod
    def points(self) -> list[ITerminalSourceOrSinkPoint]:
        """The associated signal points with this device."""

        return [e for e in self._items if isinstance(
            e, ITerminalSourceOrSinkPoint)]


class ITerminalSourceDevice(ISourceDevice, ITerminalSourceOrSinkDevice):
    """Represents a device consisting of one or more terminal source signal
    points."""

    @property
    @abstractmethod
    def points(self) -> list[ITerminalSourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items if isinstance(
            e, ITerminalSourcePoint)]


class ITerminalSinkDevice(ISinkDevice, ITerminalSourceOrSinkDevice):
    """Represents a device consisting of one or more terminal sink signal
    points."""

    @property
    @abstractmethod
    def points(self) -> list[ITerminalSinkPoint]:
        """The associated signal sink points with this device."""

        return [e for e in self._items if isinstance(
            e, ITerminalSinkPoint)]


class ITerminalDevice(ITerminalSourceDevice, ITerminalSinkDevice, IDevice):
    """Represents a device consisting of one or more terminal source and sink
    points."""

    @property
    def sources(self) -> list[ITerminalSourcePoint]:
        """The associated signal source points with this device."""

        return [e for e in self._items if isinstance(e, ITerminalSourcePoint)]

    @property
    def sinks(self) -> list[ITerminalSinkPoint]:
        """The associated signal sink points with this device."""

        return [e for e in self._items if isinstance(e, ITerminalSinkPoint)]


class IChannel(ISinkDevice):
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


class IBusSourceOrSinkPoint(ISourceOrSinkPoint):
    """Represents a signal point entering or leaving a bus."""


class IBusSourcePoint(ISourcePoint):
    """Represents signal point leaving a bus.

    This is the bus output.
    """


class IBusSinkPoint(ISinkPoint):
    """Represents signal point entering a bus.

    This is the bus input.
    """


class IBusDevice(IDevice):
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
