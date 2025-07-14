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

"""Module app_ctx."""

from __future__ import annotations
from enum import StrEnum, auto
from threading import Lock

from typing import ClassVar
from typing import final

from biz.dfch.logging import log

from .audio import RecordingParameters
from .audio import AudioDeviceInfo
from .date_time_name_input import DateTimeNameInput
from .input_device_map import InputDeviceMap
from .public.storage import StorageDeviceInfo
from .public.storage import StorageDeviceMap
from .public.storage import StorageDevice
from .public.audio import AudioDevice, AudioDeviceMap
from .public.mixer import InputOrOutput
from .public.ui import UiParameters


@final
class ApplicationContext:  # pylint: disable=R0903,R0902
    """Global ApplicationContext.

    Attributes:
        notification (AppNotification): Notification facility.
        ui_parameters (UiParameters): Contains UI parameters of the
            application.
        date_time_name_input (DateTimeNameInput): Date, time and track
            information.
        audio_device_map (AudioDeviceMap): USB to device identifier mapping.
        storage_device_map (StorageDeviceMap): USB to device identifier mapping.
        input_device_map (InputDeviceMap): USB to device identifier mapping.
        recording_parameters (RecordingParameters): Selected recording
            parameters.
        audio_configuration_map (dict[AudioDevices, SetupDevice]): Contains
            configuration parameters of audio devices.
        storage_configuration_map (dict[RcDevices, BlockDeviceType]): Contains
            configuratoin parameters of storage devices.
    """

    class Keys(StrEnum):
        """Keys in this class."""

        UI = auto()
        AUDIO_MAP = auto()
        STORAGE_MAP = auto()
        INPUT_MAP = auto()
        REC = auto()
        DAT = auto()
        AUDIO_CFG = auto()
        STORAGE_CFG = auto()
        INPUT_CFG = auto()
        XPUTS = auto()

    _instance = None
    _lock = Lock()

    ui_parameters: UiParameters
    date_time_name_input: DateTimeNameInput
    audio_device_map: AudioDeviceMap
    storage_device_map: StorageDeviceMap
    input_device_map: InputDeviceMap
    recording_parameters: RecordingParameters
    audio_configuration_map: dict[AudioDevice, AudioDeviceInfo]
    storage_configuration_map: dict[StorageDevice, StorageDeviceInfo]
    xputs: set[InputOrOutput]

    def __init__(self):
        """Private ctor. Use Factory to create an instance of this object."""

        if not ApplicationContext.Factory._lock.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initialising application context ...")

        self.ui_parameters = UiParameters()
        self.date_time_name_input = DateTimeNameInput()
        self.audio_device_map = {}
        self.storage_device_map = {}
        self.input_device_map = {}
        self.recording_parameters = RecordingParameters()
        self.audio_configuration_map = {}
        self.storage_configuration_map = {}
        self.xputs = set()

        log.info("Initialising application context SUCCEEDED. [%s]", self)

    def __str__(self) -> str:
        result = {
            ApplicationContext.Keys.UI: self.ui_parameters,
            ApplicationContext.Keys.AUDIO_MAP: self.audio_device_map,
            ApplicationContext.Keys.STORAGE_MAP: self.storage_device_map,
            ApplicationContext.Keys.INPUT_MAP: self.input_device_map,
            ApplicationContext.Keys.REC: self.recording_parameters,
            ApplicationContext.Keys.DAT: str(self.date_time_name_input),
            ApplicationContext.Keys.AUDIO_CFG: self.audio_configuration_map,
            ApplicationContext.Keys.STORAGE_CFG: self.storage_configuration_map,
            ApplicationContext.Keys.INPUT_CFG: self.storage_configuration_map,
            ApplicationContext.Keys.XPUTS: self.xputs,
        }

        return str(result)

    # pylint: disable=R0903
    class Factory:
        """Factory class."""

        __instance: ClassVar[ApplicationContext] = None
        _lock: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> ApplicationContext:
            """Returns the singleton instance."""

            if ApplicationContext.Factory.__instance is not None:
                return ApplicationContext.Factory.__instance

            with ApplicationContext.Factory._lock:

                if ApplicationContext.Factory.__instance is not None:
                    return ApplicationContext.Factory.__instance

                ApplicationContext.Factory.__instance = ApplicationContext()

            return ApplicationContext.Factory.__instance
