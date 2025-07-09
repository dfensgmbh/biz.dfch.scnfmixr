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
from ...text import UdevadmInfoVisitor

from .detecting_rc_worker_base import DetectingRcWorkerBase


class DetectingRc1Worker(DetectingRcWorkerBase):  # pylint: disable=R0903
    """Implements the logic from `DetectingRc1`."""

    _USB_DEVICE_TYPE = "usb-storage"

    _SYS_BUS_USB_DEVICES_PATH = "/sys/bus/usb/devices/"
    _VENDOR_ID_FILENAME = "idVendor"

    def select(self) -> str:
        """Selects a matching interface and returns it device path.

        Returns
            str: The device path of an HID input event device that matches the
                value specified in the ctor call.
        """

        candidates: list[UdevadmInfoVisitor.Data] = []

        for device in glob.glob(self._DEV_INPUT_EVENT_PATH_GLOB):

            log.debug("Retrieving udevadm info of device '%s' ...",
                      device)
            cmd: list[str] = [
                self._UDEVADM_FULLNAME,
                self._UDEVADM_OPTION_INFO,
                self._UDEVADM_OPTION_NOP_PAGER,
                self._UDEVADM_OPTION_ALL,
                self._UDEVADM_OPTION_NAME,
                device,
            ]

            process = Process.start(
                cmd, wait_on_completion=True, capture_stdout=True)

            text = process.stdout
            log.info("Retrieving udevadm info of device '%s' SUCCEEDED. [%s]",
                     device, len(text))

            log.debug("Parsing udevadm info of device '%s' ...",
                      device)
            visitor = UdevadmInfoVisitor()
            visitor.visit(text)

            result = visitor.get_result()
            log.info("Parsing udevadm info of device '%s' SUCCEEDED. [%s]",
                     device, result)

            if (
                self._value != result.usb_id
                or self._USB_DEVICE_TYPE != result.device_type
            ):
                log.debug(
                    "Selecting device '%s' as candidate FAILED [%s != %a]. "
                    "Skipping ...",
                    device,
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
                    device,
                    vendor_id,
                    vendor_ids
                )
                continue

            log.info(
                "Selecting device '%s' as candidate [usb_id %s] [name0 %s].",
                result.usb_id,
                result.name0,
                device)
            candidates.append(result)

        result = max(candidates, key=lambda e: len(e.name0), default=None)

        return result
