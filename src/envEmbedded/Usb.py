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

import os

from Text import TextUtils

from .UsbDeviceInfo import UsbDeviceInfo

__all__ = ["Usb"]


class Usb:
    """Retrieves information about connected USB devices. **OS and environment dependent**!"""

    _SYS_BUS_USB_DEVICES_BASEPATH = "/sys/bus/usb/devices/"
    _USB_ID_VENDOR = "idVendor"
    _USB_ID_PRODUCT = "idProduct"
    _USB_SERIAL = "serial"
    _USB_DEVNUM = "devnum"

    def __new__(cls, *args, **kwargs) -> TypeError:
        """Initialiser to prevent object initialisation."""
        raise TypeError("Static class cannot be instantiated.")

    @staticmethod
    def get_usbid(usbbus_id: str) -> str:
        """Returns the vendor and product id for the specified usb bus id.
        Args:
            usbbus_id (str): The specified usb bus id for the device to be looked up.
        Returns:
            str: If the usb bus id is could be found,
                returns the vendor id and product id as "1234:ABCD".
                Otherwise will raise a `FileNotFoundException`.
        """

        assert usbbus_id is not None and "" != usbbus_id.strip()

        sys_bus_usb_device_path = os.path.join(Usb._SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)

        idVendor = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_ID_VENDOR))
        idProduct = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_ID_PRODUCT))

        return f"{idVendor}:{idProduct}"

    def get_usb_device_info(usbbus_id: str) -> UsbDeviceInfo:
        """Returns the vendor and product id for the specified usb bus id.
        Args:
            usbbus_id (str): The specified usb bus id for the device to be looked up.
        Returns:
            UsbDeviceInfo: If the usb bus id is could be found,
                returns `UsbDeviceInfo` data class.
                Otherwise will raise a `FileNotFoundException`.
        """
        assert usbbus_id is not None and "" != usbbus_id.strip()

        sys_bus_usb_device_path = os.path.join(Usb._SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)

        idVendor = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_ID_VENDOR))
        idProduct = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_ID_PRODUCT))
        serial = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_SERIAL))
        devnum = int(TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, Usb._USB_DEVNUM)))

        return UsbDeviceInfo(idVendor=idVendor, idProduct=idProduct, serial=serial, devnum=devnum)
