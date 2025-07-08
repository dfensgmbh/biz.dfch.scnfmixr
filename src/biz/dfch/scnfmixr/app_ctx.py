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

import threading

from typing import final

from .app import LanguageCode
from .audio import AudioDevices, AudioDeviceMap
from .audio import RecordingParameters
from .audio import SetupDevice
from .input_device_map import InputDeviceMap
from .name_input import DateTimeNameInput
from .storage_device_map import StorageDeviceMap


@final
class ApplicationContext():
    """Global ApplicationContext.

    Attributes:
        language (LanguageCode): The elected langeuage.
        date_time_name_input (DateTimeNameInput): Date, time and track
            information.
        audio_device_map (AudioDeviceMap): USB to device identifier mapping.
        storage_device_map (StorageDeviceMap): USB to device identifier mapping.
        input_device_map (InputDeviceMap): USB to device identifier mapping.
        recording_parameters (RecordingParameters): Selected recording
            parameters.
        audio_configuration_map (dict[AudioDevices, SetupDevice]): Contains
            configuration parameters of audio devices.
    """

    _instance = None
    _lock = threading.Lock()

    language: LanguageCode
    date_time_name_input: DateTimeNameInput
    audio_device_map: AudioDeviceMap
    storage_device_map: StorageDeviceMap
    input_device_map: InputDeviceMap
    recording_parameters: RecordingParameters
    audio_configuration_map: dict[AudioDevices, SetupDevice]

    def __str__(self) -> str:
        result = {
            "language": self.language,
            "snd": self.audio_device_map,
            "sto": self.storage_device_map,
            "inp": self.input_device_map,
            "rec": self.recording_parameters,
            "dat": str(self.date_time_name_input),
            "dev": self.audio_configuration_map,
        }

        return str(result)

    def __new__(cls):
        """Thread safe instance creation."""

        if cls._instance:
            return cls._instance

        with cls._lock:

            if cls._instance:
                return cls._instance

            cls._instance = super().__new__(cls)

            # Set default values here and not in __init__. 
            # Ok. But why?
            cls.language = LanguageCode.DEFAULT
            cls.date_time_name_input = DateTimeNameInput()
            cls.audio_device_map = {}
            cls.storage_device_map = {}
            cls.input_device_map = {}
            cls.recording_parameters = None
            cls.audio_configuration_map = {}

        return cls._instance
