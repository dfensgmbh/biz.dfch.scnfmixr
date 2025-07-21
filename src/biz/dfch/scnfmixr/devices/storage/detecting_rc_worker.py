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

"""Module detecting_rc_worker."""

from __future__ import annotations
import glob
import json
import os

from text import TextUtils
from biz.dfch.logging import log
from biz.dfch.asyn import Process

from ...app import ApplicationContext
from ...public.storage import BlockDeviceType
from ...public.storage import MountPoint
from ...public.storage import StorageDevice
from ...public.storage import StorageDeviceInfo
from ...text import UdevadmInfoVisitor
from ..interface_detector_base import InterfaceDetectorBase

from .device_operations import DeviceOperations


class DetectingRcWorker(InterfaceDetectorBase):
    """Base class for detecting RC storage devices."""

    _UDEVADM_FULLNAME = "/usr/bin/udevadm"
    _UDEVADM_OPTION_INFO = "info"
    _UDEVADM_OPTION_ALL = "-a"
    _UDEVADM_OPTION_NOP_PAGER = "--no-pager"
    _UDEVADM_OPTION_NAME = "--name"

    _LSBLK_FULLNAME = "/usr/bin/lsblk"
    _LSBLK_OPTION_JSON = "--json"
    _LSBLK_OPTION_OUTPUT = "-o"
    _LSBLK_OPTION_OUTPUT_SEP = ","
    _LSBLK_OPTION_OUTPUT_NAME = "name"
    _LSBLK_OPTION_OUTPUT_TYPE = "type"
    _LSBLK_OPTION_OUTPUT_REMOVABLE = "rm"
    _LSBLK_OPTION_OUTPUT_COMBINED = _LSBLK_OPTION_OUTPUT_NAME + \
        _LSBLK_OPTION_OUTPUT_SEP + _LSBLK_OPTION_OUTPUT_TYPE + \
        _LSBLK_OPTION_OUTPUT_SEP + _LSBLK_OPTION_OUTPUT_REMOVABLE

    _DEV_PATH: str = "/dev/"
    _DEV_STORAGE_PREFIX: str = "sd"
    _DEV_STORAGE_PATH_GLOB: str = (
        _DEV_PATH + _DEV_STORAGE_PREFIX + "*")

    _USB_DEVICE_TYPE = "usb-storage"

    _SYS_BUS_USB_DEVICES_PATH = "/sys/bus/usb/devices/"
    _VENDOR_ID_FILENAME = "idVendor"
    _PRODUCT_ID_FILENAME = "idProduct"

    _app_ctx: ApplicationContext
    _device: StorageDevice
    _requested_usb_id: str
    _event_device_candidates: list[str]

    _usb3_to_usb2_map: dict[str, str] = {
        "4": "3",
        "2": "1"
    }

    def __init__(self, device: StorageDevice, value: str):
        """Tries to detect a storage device at the given usb_id.
        Args:
            device (str): The storage device to process.
            value (str): The usb id where the device is to be detected.
        """
        super().__init__()

        assert device and isinstance(device, StorageDevice)
        assert value and value.strip()

        self._app_ctx = ApplicationContext.Factory.get()
        self._device = device
        self._requested_usb_id = value

        self._event_device_candidates = []

    def _get_removable_devices(self) -> list[StorageDeviceInfo]:

        result: list[DetectingRcWorker.StorageDeviceInfo] = []

        def recurse(items):
            """ Finds all items with rm == true.\
{
   "blockdevices": [
      {
         "name": "sda",
         "rm": true,
         "type": "disk",
         "children": [
            {
               "name": "sda1",
               "rm": true,
               "type": "part"
            }
         ]
      },{
         "name": "mmcblk0",
         "rm": false,
         "type": "disk",
         "children": [
            {
               "name": "mmcblk0p1",
               "rm": false,
               "type": "part"
            },{
               "name": "mmcblk0p2",
               "rm": false,
               "type": "part"
            }
         ]
      }
   ]
}
"""

            for item in items:

                if item.get(self._LSBLK_OPTION_OUTPUT_NAME) is True:
                    device = StorageDeviceInfo(
                        item.get(self._LSBLK_OPTION_OUTPUT_NAME),
                        f"{self._DEV_PATH}"
                        f"{item.get(self._LSBLK_OPTION_OUTPUT_NAME)}",
                        BlockDeviceType(
                            item.get(self._LSBLK_OPTION_OUTPUT_TYPE)))
                    result.append(device)

                if "children" in device:
                    recurse(item["children"])

        cmd: list[str] = [
            self._LSBLK_FULLNAME,
            self._LSBLK_OPTION_OUTPUT,
            self._LSBLK_OPTION_OUTPUT_COMBINED,
            self._LSBLK_OPTION_JSON,
        ]

        process = Process.start(
            cmd, wait_on_completion=True, capture_stdout=True)

        text = process.stdout

        x = '\n'.join(text)
        log.debug("type '%s'. __%s__", type(x), x)
        recurse(json.load(x))

        return result

    def select(self) -> str | None:
        """Selects a matching interface and returns it device path.

        Returns
            str: The device path of an storqage device that matches the
                value specified in the ctor call.
        """

        candidates: list[UdevadmInfoVisitor.Data] = []

        devices = glob.glob(self._DEV_STORAGE_PATH_GLOB)
        # devices = [d.name for d in self._get_removable_devices()]
        for full_name in devices:

            log.debug("Retrieving udevadm info of device '%s' ...",
                      full_name)
            cmd: list[str] = [
                self._UDEVADM_FULLNAME,
                self._UDEVADM_OPTION_INFO,
                self._UDEVADM_OPTION_NOP_PAGER,
                self._UDEVADM_OPTION_ALL,
                self._UDEVADM_OPTION_NAME,
                full_name,
            ]

            process = Process.start(
                cmd, wait_on_completion=True, capture_stdout=True)

            text = process.stdout
            log.info("Retrieving udevadm info of device '%s' OK. [%s]",
                     full_name, len(text))

            log.debug("Parsing udevadm info of device '%s' ...",
                      full_name)
            visitor = UdevadmInfoVisitor()
            visitor.visit(text)

            result = visitor.get_result()
            log.info("Parsing udevadm info of device '%s' OK. [%s]",
                     full_name, result)

            key = self._requested_usb_id[0]
            assert key and key.isdigit()
            mapped_id = self._usb3_to_usb2_map.get(key, key)
            mapped_usb_id = mapped_id + self._requested_usb_id[1:]

            usb_id_mismatch = result.usb_id not in (
                self._requested_usb_id, mapped_usb_id)
            type_mismatch = self._USB_DEVICE_TYPE != result.device_type

            if usb_id_mismatch or type_mismatch:

                log.debug(
                    "Selecting device '%s' as candidate FAILED "
                    "[%sa != (%sr | %sm)]. "
                    "Skipping ...",
                    full_name,
                    result.usb_id,
                    self._requested_usb_id,
                    mapped_usb_id,
                )
                continue

            filename = os.path.join(
                self._SYS_BUS_USB_DEVICES_PATH,
                result.usb_id,
                self._VENDOR_ID_FILENAME)
            vendor_id = TextUtils().read_first_line(filename).lower()
            filename = os.path.join(
                self._SYS_BUS_USB_DEVICES_PATH,
                result.usb_id,
                self._PRODUCT_ID_FILENAME)
            product_id = TextUtils().read_first_line(filename).lower()

            whitelist = self._app_ctx.storage_parameters.allowed_usb_ids
            is_match = any(
                (pid is None or pid == product_id) and vid == vendor_id
                for vid, pid in whitelist
            )

            if not is_match:
                log.debug(
                    "Selecting device '%s' as candidate FAILED [%s not in %s]. "
                    "Skipping ...",
                    full_name,
                    vendor_id,
                    whitelist
                )
                continue

            log.info(
                "Selecting device '%s' as candidate [usb_id %s] [name0 %s].",
                result.usb_id,
                result.name0,
                full_name)
            candidates.append(result)

        result = max(candidates, key=lambda e: len(e.name0), default=None)

        if result is None:
            log.error("No storage device found at '%s'.",
                      self._requested_usb_id)
            return None

        # Note: we have to change the logic to start enumerating via lsblk and
        # then select the device.
        # Until then, we have to manually construct the StorageDeviceInfo.
        # And for that, as of now we have to assume the type: partition.
        # Yes, I know ...
        device_info = StorageDeviceInfo(
            result.name0,
            os.path.join(self._DEV_PATH, result.name0),
            # Fix this!
            BlockDeviceType.PARTITION.value,
            MountPoint[self._device.name].value)

        self._app_ctx.storage_configuration_map[self._device] = device_info

        is_mounted = DeviceOperations(device_info).mount()

        return result if is_mounted else None
