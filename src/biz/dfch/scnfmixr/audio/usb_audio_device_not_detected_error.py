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

"""Module usb_audio_device_not_detected_error."""


class UsbAudioDeviceNotDetectedError(Exception):
    """Exception for failed USB audio device detection."""

    message: str
    usb_id: str

    def __init__(self, usb_id: str | None = None):
        if usb_id:
            message = (
                f"USB audio device not detected at '{usb_id}'."
            )
        else:
            message = "USB audio device not detected."

        super().__init__(message)

        self.message = message
        self.usb_id = usb_id

    def __str__(self) -> str:
        return self.message

    def __repr__(self):
        return self.__str__()
