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

"""Contains information about an ALSA USB device as seen in `/proc/asound`."""

from dataclasses import dataclass
import re
from typing import Any

__all__ = ["ProcAlsaUsbDeviceInfo"]

_USBBUS_PATTERN = r"^(\d+)/(\d+)$"
_USBBUS_PATTERN_BUSNUM_IDX = 1
_USBBUS_PATTERN_DEVNUM_IDX = 2


@dataclass(frozen=True)
class ProcAlsaUsbDeviceInfo:
    """Contains information about an ALSA USB device as seen in `/proc/asound`.

    Attributes:
        card_id (int): The ALSA card id of the device.
        display_name (str): The ALSA `id` of the device. This can change
            between reconnects.
        usbbus (str): The USB bus and device number of the device.
        usbid (str): The USB vendor and product id of the device.

    Notes:
        To retrieve the bus and device number as `int` use the respective `get_`
            methods.
        To retrieve vendor and product id separately use the respective `get_`
            methods.
    """

    card_id: int = 0
    display_name: str = ""
    usbbus: str = ""
    usbid: str = ""

    def get_busnum(self) -> int:
        """Returns the bus number of the device.

        Returns:
            int: The bus number of the device.
        """

        match = re.match(_USBBUS_PATTERN, self.usbbus)
        if not match:
            raise ValueError

        return int(match.group(_USBBUS_PATTERN_BUSNUM_IDX))

    def get_devnum(self) -> int:
        """Returns the device number on the usbbus of the device.

        Returns:
            int: The device number on the usbbus of the device.
        """

        match = re.match(_USBBUS_PATTERN, self.usbbus)
        if not match:
            raise ValueError

        return int(match.group(_USBBUS_PATTERN_DEVNUM_IDX))

    def get_id_vendor(self) -> str:
        """Returns the USB vendor id of the device.

        Returns:
            int: The USB vendor id of the device.
        """

        return self.usbid.split(":", maxsplit=1)[0]

    def get_id_product(self) -> str:
        """Returns the USB product id of the device.

        Returns:
            int: The USB product id of the device.
        """

        return self.usbid.split(":", maxsplit=1)[1]

    def to_dict(self) -> dict[str, Any]:
        """Converts this information into a dictionary.

        Returns:
            Dict (str, Any): A key-value map containining the ALSA stream
                information.
        """

        return {
            "card_id": self.card_id,
            "display_name": self.display_name,
            "usbbus": self.usbbus,
            "usbid": self.usbid,
            "busnum": self.get_busnum(),
            "devnum": self.get_devnum(),
            "id_vendor": self.get_id_vendor(),
            "id_product": self.get_id_product(),
        }
