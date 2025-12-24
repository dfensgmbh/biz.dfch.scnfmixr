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

"""Package mixer."""

from __future__ import annotations

from .audio_input import AudioInput
from .audio_input_or_output import AudioInputOrOutput
from .audio_output import AudioOutput
from .connection import Connection
from .constant import Constant
from .input_or_output import InputOrOutput
from .input import Input
from .output import Output
from .file_input_or_output import FileInputOrOutput
from .file_input import FileInput
from .file_output import FileOutput
from .connection_info import ConnectionInfo

from .iacquirable import IAcquirable

from .connection_policy import ConnectionPolicy
from .connection_policy_exception import ConnectionPolicyException

from .iconnectable_point_or_set import IConnectablePointOrSet
from .iconnectable_point import IConnectablePoint
from .iconnectable_set import IConnectableSet

from .iconnectable_source import IConnectableSource
from .iconnectable_source_point import IConnectableSourcePoint
from .iconnectable_source_set import IConnectableSourceSet

from .iconnectable_sink import IConnectableSink
from .iconnectable_sink_point import IConnectableSinkPoint
from .iconnectable_sink_set import IConnectableSinkSet
from .isignal_path import ISignalPath

from .iterminal_source_or_sink_device import ITerminalSourceOrSinkDevice
from .iterminal_source_device import ITerminalSourceDevice
from .iterminal_sink_device import ITerminalSinkDevice
from .iterminal_device import ITerminalDevice

from .iterminal_source_or_sink_point import ITerminalSourceOrSinkPoint
from .iterminal_source_point import ITerminalSourcePoint
from .iterminal_sink_point import ITerminalSinkPoint

from .state import State

from .iconnectable_source_or_sink_device import IConnectableSourceOrSinkDevice
from .iconnectable_source_device import IConnectableSourceDevice
from .iconnectable_sink_device import IConnectableSinkDevice
from .iconnectable_device import IConnectableDevice

from .source_set_view import SourceSetView
from .sink_set_view import SinkSetView
from .mixbus_device import (
    MixbusDevice,
    IsoChannelDry,
    IsoChannelWet,
)


__all__ = [
    "IAcquirable",
    "ConnectionPolicy",
    "ConnectionPolicyException",
    "IConnectablePointOrSet",
    "IConnectablePoint",
    "IConnectableSet",
    "IConnectableSource",
    "IConnectableSourcePoint",
    "IConnectableSourceSet",
    "IConnectableSink",
    "IConnectableSinkPoint",
    "IConnectableSinkSet",
    "ISignalPath",

    "IConnectableSourceOrSinkDevice",
    "IConnectableSourceDevice",
    "IConnectableSinkDevice",
    "IConnectableDevice",
    "SourceSetView",
    "SinkSetView",

    "ITerminalSourceOrSinkDevice",
    "ITerminalSourceDevice",
    "ITerminalSinkDevice",
    "ITerminalDevice",
    "ITerminalSourceOrSinkPoint",
    "ITerminalSourcePoint",
    "ITerminalSinkPoint",

    "State",

    "Connection",
    "ConnectionInfo",
    "Constant",
    "InputOrOutput",
    "Input",
    "Output",
    "FileInputOrOutput",
    "FileInput",
    "FileOutput",
    "AudioInputOrOutput",
    "AudioInput",
    "AudioOutput",

    "MixbusDevice",
    "IsoChannelDry",
    "IsoChannelWet",
]
