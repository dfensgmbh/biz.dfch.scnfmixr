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

"""Module isignal_path."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .iacquirable import IAcquirable
from .iconnectable_sink_point import IConnectableSinkPoint
from .iconnectable_source_point import IConnectableSourcePoint


@dataclass(frozen=True)
class ISignalPath(IAcquirable, ABC):
    """Represents a signal path from a source signal point to sink signal
    point.

    Attributes:
        name (str): The name of the signal path.
        source (IConnectableSourcePoint): One side of the signal path.
        sink (IConnectableSinkPoint): The other side of the signal path.
    """

    _CONNECTION_SEPARATOR = '+'
    _NAME_DELIMITER = "'"

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

        assert isinstance(source, IConnectableSourcePoint)
        assert isinstance(sink, IConnectableSinkPoint)
        assert source.is_point
        assert sink.is_sink

        object.__setattr__(self, "name",
                           ISignalPath.get_connection_name(
                               source.name, sink.name))
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "sink", sink)

    @staticmethod
    def get_connection_name(source: str, sink: str) -> str:
        """Create a connection name from a source and a sink name."""

        assert isinstance(source, str) and source.strip()
        assert isinstance(sink, str) and sink.strip()

        return (
            # f"{ISignalPath._NAME_DELIMITER}"
            f"{source}"
            # f"{ISignalPath._NAME_DELIMITER}"
            f"{ISignalPath._CONNECTION_SEPARATOR}"
            # f"{ISignalPath._NAME_DELIMITER}"
            f"{sink}"
            # f"{ISignalPath._NAME_DELIMITER}"
        )

    @staticmethod
    def split_connection_name(value: str) -> tuple[str, str]:
        """Splits a connection name into source and sink name."""

        assert isinstance(value, str) and value.strip()

        quoted_names = value.strip(ISignalPath._CONNECTION_SEPARATOR)
        source = quoted_names[0].strip(ISignalPath._NAME_DELIMITER)
        sink = quoted_names[1].strip(ISignalPath._NAME_DELIMITER)

        return (source, sink)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """Determines whether the signal path is active."""
