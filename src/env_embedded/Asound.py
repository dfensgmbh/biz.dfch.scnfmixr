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
import re


from .AsoundCardInfo import AsoundCardInfo
from .UsbDeviceInfo import UsbDeviceInfo
from text import TextUtils
from log import log

__all__ = ["Asound"]


class Asound:

    @staticmethod
    def get_info(usbDeviceInfo: UsbDeviceInfo) -> AsoundCardInfo | None:
        """Returns a `AsoundCardInfo` class for the device specified in `usbDeviceInfo`.
        Args:
            usbDeviceInfo (UsbDeviceInfo): The device to get information about.
        Returns:
            AsoundCardInfo?: Returns `AsoundCardInfo`
                if the device specified in `usbDeviceInfo` could be found. Otherwise returns `None.
        """

        PROC_ASOUND_BASEPATH = "/proc/asound/"
        CARD_PATTERN = r"^card(\d+)$"
        USBBUS_PATTERN = r"^(\d+)/(\d+)$"

        target_usbid = f"{usbDeviceInfo.idVendor}:{usbDeviceInfo.idProduct}"

        for card_dir_basename in os.listdir(PROC_ASOUND_BASEPATH):
            try:
                match = re.match(CARD_PATTERN, card_dir_basename)
                if not match:
                    continue

                card_id = int(match.group(1))
                card_dir_fullpath = os.path.join(PROC_ASOUND_BASEPATH, card_dir_basename)

                # Test if specified usbid matches current card.
                usbid = TextUtils().read_first_line(os.path.join(card_dir_fullpath, "usbid"))
                if usbid.lower() != target_usbid.lower():
                    continue

                # Test if specified devnum matches current card.
                usbbus = TextUtils().read_first_line(os.path.join(card_dir_fullpath, "usbbus"))
                match = re.match(USBBUS_PATTERN, usbbus)
                if not match:
                    continue
                devnum = int(match.group(2))
                if devnum != usbDeviceInfo.devnum:
                    continue

                log.info(f"Card '{card_id}' found for '{target_usbid}' ['{devnum}']")
                return AsoundCardInfo(usbDeviceInfo=usbDeviceInfo, idCard=card_id)

            except Exception:
                continue

        log.warning(f"Card id not found for '{target_usbid}' ['{devnum}']")
        return None
