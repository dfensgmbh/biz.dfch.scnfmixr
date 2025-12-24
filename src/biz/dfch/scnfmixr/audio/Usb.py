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

"""
This module provide USB device related functions.
"""

import os
from typing import NoReturn

from biz.dfch.logging import log

from text import TextUtils
from ..public.usb import UsbDeviceInfo
from .proc_alsa_usb_device_info import ProcAlsaUsbDeviceInfo

__all__ = [
    "Usb",
]


class Usb:
    """Retrieves information about connected USB devices.

    **OS and environment dependent!**
    """

    _SYS_BUS_USB_DEVICES_BASEPATH = "/sys/bus/usb/devices/"
    _USB_MANUFACTURER = "manufacturer"
    _USB_PRODUCT = "product"
    _USB_VERSION = "version"
    _USB_ID_VENDOR = "idVendor"
    _USB_ID_PRODUCT = "idProduct"
    _USB_BUSNUM = "busnum"
    _USB_DEVNUM = "devnum"

    def __new__(cls, *_args, **_kwargs) -> NoReturn:
        """Initialiser to prevent object instantiation."""

        _ = _args
        _ = _kwargs

        raise TypeError("Static class cannot be instantiated.")

    @staticmethod
    def get_best_device_name(
        usb_id: str,
        devices: dict[str, ProcAlsaUsbDeviceInfo]
    ) -> str | None:
        """Gets the best matching USB device id based on `devices` map.
        Args:
            usb_id (str): A USB id, e.g `1-1.2.1`, `3-1`.
            devices (dict[ProcAlsaUsbDeviceInfo]): A map of USB device ids and
                ALSA card information.
        Returns:
            str: The USB device id that matches best from the specified
                `devices` map. `None` if none of the `devices` match.
        Notes:
            The best matching USB device id is the shortest key that starts
            with `usb_id` (case-sensitive) and is also alphabetically first.
        """

        assert usb_id and usb_id.strip()
        assert devices is not None

        candidates = [
            name for name in sorted(devices.keys()) if name.startswith(usb_id)
        ]

        if not candidates:
            return None

        return min(candidates, key=len)

    @staticmethod
    def get_usbid(usbbus_id: str) -> str:
        """Returns the vendor and product id for the specified usb bus id.
        Args:
            usbbus_id (str): The specified usb bus id for the device to be
                looked up.
        Returns:
            str: If the usb bus id is could be found,
                returns the vendor id and product id as "1234:ABCD".
                Otherwise will raise a `FileNotFoundException`.
        """

        assert usbbus_id and usbbus_id.strip()

        sys_bus_usb_device_path = os.path.join(
            Usb._SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)

        id_vendor = TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_ID_VENDOR))
        id_product = TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_ID_PRODUCT))

        return f"{id_vendor}:{id_product}"

    @staticmethod
    def get_usb_device_info(usbbus_id: str) -> UsbDeviceInfo:
        """Returns the vendor and product id for the specified usb bus id.

        Args:
            usbbus_id (str): The specified usb bus id for the device to be
                looked up.

        Returns:
            UsbDeviceInfo: If the usb bus id is could be found,
                returns `UsbDeviceInfo` data class.
                Otherwise will raise a `FileNotFoundException`.
        """
        assert usbbus_id and usbbus_id.strip()

        sys_bus_usb_device_path = os.path.join(
            Usb._SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)

        manufacturer = TextUtils().try_read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_MANUFACTURER))
        product = TextUtils().try_read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_PRODUCT))
        version = TextUtils().try_read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_VERSION))
        id_vendor = TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_ID_VENDOR))
        id_product = TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_ID_PRODUCT))
        busnum = int(TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_BUSNUM)))
        devnum = int(TextUtils().read_first_line(
            os.path.join(sys_bus_usb_device_path, Usb._USB_DEVNUM)))

        log.debug("%s: [%s:%s] [%s-%s]", usbbus_id,
                  id_vendor, id_product, busnum, devnum)

        return UsbDeviceInfo(
            manufacturer=manufacturer or "",
            product=product or "",
            version=version or "",
            id_vendor=id_vendor,
            id_product=id_product,
            busnum=busnum,
            devnum=devnum,
        )

    @staticmethod
    def get_alsa_usb_device_map(
        devices: list[ProcAlsaUsbDeviceInfo]
    ) -> dict[str, ProcAlsaUsbDeviceInfo]:
        """Retrieves a map of ALSA USB device names based on the given list of
        ALSA USB device information.

        Args:
            devices (list[ProcAlsaUsbDeviceInfo]): A list of ALSA USB devices.

        Returns:
            dict (str, ProcAlsaUsbDeviceInfo): A map with the ALSA device info
            given by `devices` as values and the USB device name as keys.

        Notes:
            `devices` must contain unique device information and not have
            duplicates.
        """

        assert devices is not None

        result: dict[str, ProcAlsaUsbDeviceInfo] = {}

        devices_and_interfaces = os.listdir(Usb._SYS_BUS_USB_DEVICES_BASEPATH)

        for alsa_device in devices:
            for device in devices_and_interfaces:

                # Only process devices and not interfaces
                if ":" in device:
                    continue

                # Only process device names not already in the result
                if device in result:
                    continue

                path_name = os.path.join(
                    Usb._SYS_BUS_USB_DEVICES_BASEPATH, device)
                log.debug("Processing '%s' ...", path_name)

                file_name = os.path.join(path_name, Usb._USB_ID_VENDOR)
                id_vendor = TextUtils().try_read_first_line(file_name)
                if id_vendor != alsa_device.get_id_vendor():
                    continue

                file_name = os.path.join(path_name, Usb._USB_ID_PRODUCT)
                id_product = TextUtils().try_read_first_line(file_name)
                if id_product != alsa_device.get_id_product():
                    continue

                file_name = os.path.join(path_name, Usb._USB_BUSNUM)
                busnum = int(TextUtils().try_read_first_line(file_name))
                if busnum != alsa_device.get_busnum():
                    continue

                file_name = os.path.join(path_name, Usb._USB_DEVNUM)
                devnum = int(TextUtils().try_read_first_line(file_name))
                if devnum != alsa_device.get_devnum():
                    continue

                log.debug(
                    "Found %s: '%s' [%s] [%s:%s] [%s-%s]",
                    device,
                    alsa_device.display_name,
                    alsa_device.card_id,
                    alsa_device.get_id_vendor(),
                    alsa_device.get_id_product(),
                    alsa_device.get_busnum(),
                    alsa_device.get_devnum(),
                )
                assert device not in result

                result[device] = alsa_device
                break

        return result
