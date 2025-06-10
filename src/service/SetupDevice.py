# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

"""Module implementing device detection and setup."""

from __future__ import annotations
import time

from env_embedded import Asound, Usb
from log import log

__all__ = ["SetupDevice"]


class SetupDevice:
    """Detects and sets up a ALSA USB device."""

    class Factory:
        """Factory class for creating `SetupDevice` instances."""

        @staticmethod
        def create(usb_id: str, max_attempts: int = 0, wait_interval_ms: int = 1000) -> SetupDevice:
            """Factory method for creating `SetupDevice` instances.
            Args:
                usb_id (str): The USB id to detect and setup.
                max_attempts (int): The maximum number of attempts to detect and setup the device.
                    If `0` is specified, an infinite number of attempts is made.
                wait_interval_ms (int): Time in milliseconds to wait between attempts.
            Returns:
                SetupDevice: A successfully created device instance.
            Raises:
                RuntimeError: If the device could not be created within the given number of attempts.
            """

            assert usb_id is not None and "" != usb_id
            assert 0 <= max_attempts
            assert 0 <= wait_interval_ms

            current_attempt = 0

            while True:
                try:

                    return SetupDevice(usb_id)

                except Exception as ex:  # pylint: disable=broad-exception-caught

                    current_attempt += 1
                    if max_attempts and current_attempt >= max_attempts:
                        message = f"Usb '{usb_id}' not detected [{current_attempt}/{max_attempts}]."
                        log.error(message)
                        raise RuntimeError(message) from ex

                    log.debug(
                        "Usb '%s' not detected. Waiting %s ms [%s/%s].",
                        usb_id,
                        wait_interval_ms,
                        current_attempt,
                        max_attempts,
                    )
                    time.sleep(wait_interval_ms / 1000.0)

    def __init__(self, usb_id: str):

        assert usb_id is not None and "" != usb_id.strip()

        self.requested_usb_id = usb_id

        # Retrieve all connected ALSA USB devices.
        alsa_devices = Asound.get_devices()

        # Get USB device names for ALSA USB devices.
        usb_name_alsa_device_map = Usb.get_alsa_usb_device_map(alsa_devices)
        self.actual_usb_id = Usb.get_best_device_name(self.requested_usb_id, usb_name_alsa_device_map)

        if self.actual_usb_id is None:
            message = f"Requested USB id '{self.requested_usb_id} not found."
            log.error(message)
            raise RuntimeError(message)

        log.info("Mapped requested usb_id: [%s / %s]", self.requested_usb_id, self.actual_usb_id)

        log.info("Trying to detect device on '%s' ...", self.actual_usb_id)
        self.device_info = Usb.get_usb_device_info(self.actual_usb_id)
        self.asound_info = Asound.get_info(self.device_info)
