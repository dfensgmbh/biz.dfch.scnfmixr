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

from .path_state import PathState
from .path_state_flag import PathStateFlag

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

    "PathState",
    "PathStateFlag",

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
]
