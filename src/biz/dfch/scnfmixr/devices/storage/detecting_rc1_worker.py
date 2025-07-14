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

"""Module detecting_rc1_worker."""

import glob
import os

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from text import TextUtils
from ...application_context import ApplicationContext
from ...public.storage import StorageDevice
from ...public.storage import BlockDeviceType
from ...public.storage import StorageDeviceInfo
from ...text import UdevadmInfoVisitor

from .detecting_rc_worker_base import DetectingRcWorkerBase
from .device_operations import DeviceOperations
from .mount_point import MountPoint


class DetectingRc1Worker(DetectingRcWorkerBase):  # pylint: disable=R0903
    """Implements the logic from `DetectingRc1`."""

    _USB_DEVICE_TYPE = "usb-storage"

    _DEV_PATH = "/dev/"
    _SYS_BUS_USB_DEVICES_PATH = "/sys/bus/usb/devices/"
    _VENDOR_ID_FILENAME = "idVendor"

    def select(self) -> str | None:
        """Selects a matching interface and returns it device path.

        Returns
            str: The device path of an storqage device that matches the
                value specified in the ctor call.
        """

        app_ctx = ApplicationContext.Factory.get()

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

            if (
                self._value != result.usb_id
                or self._USB_DEVICE_TYPE != result.device_type
            ):
                log.debug(
                    "Selecting device '%s' as candidate FAILED [%s != %a]. "
                    "Skipping ...",
                    full_name,
                    self._value,
                    result.usb_id
                )
                continue

            # Checking for vendor id.
            # DFTODO: Read from CLI args.
            vendor_ids: list[str] = [
                "2009",
            ]

            filename = os.path.join(
                self._SYS_BUS_USB_DEVICES_PATH,
                result.usb_id,
                self._VENDOR_ID_FILENAME)
            vendor_id = TextUtils().read_first_line(filename)

            if vendor_id not in vendor_ids:
                log.debug(
                    "Selecting device '%s' as candidate FAILED [%s not in %a]. "
                    "Skipping ...",
                    full_name,
                    vendor_id,
                    vendor_ids
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
            log.error("No storage device found at '%s'.", self._value)
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
            MountPoint.RC1.value)

        app_ctx.storage_configuration_map[StorageDevice.RC1] = device_info

        is_mounted = DeviceOperations(device_info).mount()

        return result if is_mounted else None
