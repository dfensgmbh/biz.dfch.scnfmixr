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

"""Module implementing sound device detection and setup."""

from __future__ import annotations
import time

from biz.dfch.logging import log
from .usb_audio_device_not_detected_error import UsbAudioDeviceNotDetectedError
from ..alsa_usb import AlsaStreamInfoParser
from ..public.usb import UsbDeviceInfo
from ..public.audio import AlsaInterfaceInfo
from ..public.audio import Format
from ..public.audio import SampleRate
from .Asound import Asound
from .asound_card_info import AsoundCardInfo
from .Usb import Usb


__all__ = [
    "AudioDeviceInfo",
]


class AudioDeviceInfo:  # pylint: disable=R0903
    """Detects and sets up a ALSA USB device.

    Attributes:
        requested_usb_id (str): The requested USB id of the sound device.
        actual_usb_id (str): The actual USB id of the sound device.
        device_info (UsbDeviceInfo): Contains USB device information.
        asound_info (AsoundCardInfo): Contains ALSA device information.
        source (AlsaInterfaceInfo): Contains interface information about the
            ALSA capture device.
        sink (AlsaInterfaceInfo): Contains interface information about the
            ALSA playback device.
    """

    requested_usb_id: str
    actual_usb_id: str
    device_info: UsbDeviceInfo
    asound_info: AsoundCardInfo
    source: AlsaInterfaceInfo
    sink: AlsaInterfaceInfo

    class Factory:  # pylint: disable=R0903
        """Factory class for creating `AudioDeviceInfo` instances."""

        @staticmethod
        def create(
            usb_id: str,
            max_attempts: int = 0,
            wait_interval_ms: int = 1000
        ) -> AudioDeviceInfo:
            """Factory method for creating `AudioDeviceInfo` instances.

            Args:
                usb_id (str): The USB id to detect and setup.
                max_attempts (int): The maximum number of attempts to detect
                    and setup the device. If `0` is specified, an infinite
                    number of attempts is made.
                wait_interval_ms (int): Time in milliseconds to wait between
                    attempts.

            Returns:
                AudioDeviceInfo: A successfully created device instance.

            Raises:
                RuntimeError: If the device could not be created within the
                    given number of attempts.
            """

            assert usb_id and usb_id.strip()
            assert 0 <= max_attempts
            assert 0 <= wait_interval_ms

            current_attempt = 0

            while True:
                try:

                    return AudioDeviceInfo(usb_id)

                except UsbAudioDeviceNotDetectedError:  # pylint: disable=W0718

                    current_attempt += 1
                    if max_attempts and current_attempt >= max_attempts:
                        raise

                    log.debug(
                        ("USB audio device not detected at '%s'. "
                         "Waiting %s ms [%s/%s]."),
                        usb_id,
                        wait_interval_ms,
                        current_attempt,
                        max_attempts,
                    )
                    time.sleep(wait_interval_ms / 1000.0)

                except Exception as ex:

                    message = (f"USB audio device not detected at '{usb_id}'. "
                               f"[{ex}]")
                    log.error(message, exc_info=True)
                    raise RuntimeError(message) from ex

    def __init__(self, usb_id: str):

        assert usb_id and usb_id.strip()

        self.requested_usb_id = usb_id

        # Retrieve all connected ALSA USB devices.
        alsa_devices = Asound.get_devices()

        # Get USB device names for ALSA USB devices.
        usb_name_alsa_device_map = Usb.get_alsa_usb_device_map(alsa_devices)
        self.actual_usb_id = Usb.get_best_device_name(
            self.requested_usb_id, usb_name_alsa_device_map)

        if self.actual_usb_id is None:
            message = f"Requested USB id '{self.requested_usb_id} not found."
            log.error(message)
            raise UsbAudioDeviceNotDetectedError(self.requested_usb_id)

        log.info("Mapped requested usb_id: [%s / %s]",
                 self.requested_usb_id, self.actual_usb_id)

        log.debug("Detecting device on '%s' ...", self.actual_usb_id)

        self.device_info = Usb.get_usb_device_info(self.actual_usb_id)
        log.info("[usb_device_info '%s']: [%s]",
                 self.actual_usb_id, self.device_info)
        self.asound_info = Asound.get_info(self.device_info)
        log.info("[asound_card_info '%s']: [%s]",
                 self.actual_usb_id, self.asound_info)

        parser = AlsaStreamInfoParser(self.asound_info.card_id)
        capture_interface = parser.get_best_capture_interface()
        log.debug(capture_interface)
        self.source = AlsaInterfaceInfo(
            card_id=self.asound_info.card_id,
            interface_id=parser.interface_id,
            channel_count=capture_interface.channel_count,
            format=Format(capture_interface.format),
            bit_depth=Format(capture_interface.format).get_bit_depth(),
            sample_rate=SampleRate(capture_interface.get_best_rate()),
        )
        playback_interface = parser.get_best_playback_interface()
        self.sink = AlsaInterfaceInfo(
            card_id=self.asound_info.card_id,
            interface_id=parser.interface_id,
            channel_count=playback_interface.channel_count,
            format=Format(playback_interface.format),
            sample_rate=SampleRate(playback_interface.get_best_rate()),
            bit_depth=Format(playback_interface.format).get_bit_depth(),
        )

        log.info("Detecting device on '%s' OK.", self.actual_usb_id)

    def __str__(self) -> str:

        result = {
            "requested_usb_id": self.requested_usb_id,
            "actual_usb_id": self.actual_usb_id,
            "asound_info": self.asound_info,
            "source": self.source,
            "sink": self.sink,
        }

        return str(result)

    def __repr__(self) -> str:
        return self.__str__()
