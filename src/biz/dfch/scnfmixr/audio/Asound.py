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

"""Module for handling USB ASLA sound devices."""

import os
import re

from text import TextUtils

from biz.dfch.logging import log

from ..public.usb import UsbDeviceInfo
from .asound_card_info import AsoundCardInfo
from .proc_alsa_usb_device_info import ProcAlsaUsbDeviceInfo

__all__ = [
    "Asound",
]

_PROC_ASOUND_BASEPATH = "/proc/asound/"
_CARD_PATTERN = r"^card(\d+)$"
_USBBUS_PATTERN = r"^(\d+)/(\d+)$"
_USBBUS_PATTERN_BUSNUM_IDX = 1
_USBBUS_PATTERN_DEVNUM_IDX = 2

_ASOUND_CARD_USBID = "usbid"
_ASOUND_CARD_USBBUS = "usbbus"
_ASOUND_CARD_ID = "id"


class Asound:
    """Manages USB ALSA sound devices."""

    @staticmethod
    def get_device(card_id: int) -> ProcAlsaUsbDeviceInfo | None:
        """Returns a connected ALSA USB device based on its ALSA card id.

        Args:
            id_card (int): The ALSA USB card id.

        Returns:
            (ProcAlsaUsbDeviceInfo | None): The ALSA USB device or None.

        Notes:
            Even when a valid `id` is specified it will return `None` if the
            device in question is not a USB device.
        """

        assert 0 < card_id

        devices = Asound.get_devices()
        return next(
            (device for device in devices if device.card_id == card_id), None)

    @staticmethod
    def get_devices() -> list[ProcAlsaUsbDeviceInfo]:
        """Returns a list of all currently connected ALSA USB devices.

        Returns:
            list (ProcAlsaUsbDeviceInfo): The list of ALSA USB devices.
        """

        result: list[ProcAlsaUsbDeviceInfo] = []

        for card_dir_basename in os.listdir(_PROC_ASOUND_BASEPATH):

            try:
                log.debug("Enumerating card '%s' ...", card_dir_basename)
                match = re.match(_CARD_PATTERN, card_dir_basename)
                if not match:
                    continue

                log.debug("Card candidate found '%s'.", card_dir_basename)

                card_id = int(match.group(1))
                log.debug("Card candidate '%s' has card_id: '%s'.",
                          card_dir_basename, card_id)
                card_dir_fullpath = os.path.join(
                    _PROC_ASOUND_BASEPATH, card_dir_basename)

                usbid = TextUtils().read_first_line(
                    os.path.join(card_dir_fullpath, _ASOUND_CARD_USBID))
                log.debug("Card candidate '%s' has usbid: '%s'.",
                          card_dir_basename, usbid)

                usbbus = TextUtils().read_first_line(
                    os.path.join(card_dir_fullpath, _ASOUND_CARD_USBBUS))
                log.debug("Card candidate '%s' has usbbus: '%s'.",
                          card_dir_basename, usbbus)

                display_name = TextUtils().read_first_line(
                    os.path.join(card_dir_fullpath, _ASOUND_CARD_ID))
                log.debug("Card candidate '%s' has display name: '%s'.",
                          card_dir_basename, display_name)

                device_info = ProcAlsaUsbDeviceInfo(
                    card_id=card_id,
                    display_name=display_name,
                    usbbus=usbbus,
                    usbid=usbid,
                )
                log.info("ALSA USB device: %s", device_info)
                result.append(device_info)

            except Exception:  # pylint: disable=broad-exception-caught
                continue

        return result

    @staticmethod
    def get_info(info: UsbDeviceInfo) -> AsoundCardInfo | None:
        """Returns a `AsoundCardInfo` class for the device specified in
        `usbDeviceInfo`.

        Args:
            info (UsbDeviceInfo): The device to get information about.

        Returns:
            AsoundCardInfo?: Returns `AsoundCardInfo`if the device specified in
                `usbDeviceInfo` could be found. Otherwise returns `None.
        """

        target_usbid = f"{info.id_vendor}:{info.id_product}"
        log.debug("Trying to detect '%s' [%s-%s] ...",
                  target_usbid, info.busnum, info.devnum)

        for card_dir_basename in os.listdir(_PROC_ASOUND_BASEPATH):
            try:
                log.debug("Enumerating card '%s' ...", card_dir_basename)
                match = re.match(_CARD_PATTERN, card_dir_basename)
                if not match:
                    continue

                log.debug("Card candidate found '%s'.", card_dir_basename)

                card_id = int(match.group(1))
                log.debug("Card candidate '%s' has card_id: '%s'.",
                          card_dir_basename, card_id)
                card_dir_fullpath = os.path.join(
                    _PROC_ASOUND_BASEPATH, card_dir_basename)

                # Test if specified usbid matches current card.
                usbid = TextUtils().read_first_line(
                    os.path.join(card_dir_fullpath, _ASOUND_CARD_USBID))
                log.debug("Card candidate '%s' has usbid: '%s'.",
                          card_dir_basename, usbid)
                if usbid.lower() != target_usbid.lower():
                    continue

                usbbus = TextUtils().read_first_line(
                    os.path.join(card_dir_fullpath, _ASOUND_CARD_USBBUS))
                log.debug("Card candidate '%s' has usbbus: '%s'.",
                          card_dir_basename, usbbus)
                match = re.match(_USBBUS_PATTERN, usbbus)
                if not match:
                    continue

                # Test if specified busnum matches current card.
                busnum = int(match.group(_USBBUS_PATTERN_BUSNUM_IDX))
                log.debug("Card candidate '%s' has busnum: '%s'.",
                          card_dir_basename, busnum)
                if busnum != info.busnum:
                    continue

                # Test if specified devnum matches current card.
                devnum = int(match.group(_USBBUS_PATTERN_DEVNUM_IDX))
                log.debug("Card candidate '%s' has devnum: '%s'.",
                          card_dir_basename, devnum)
                if devnum != info.devnum:
                    continue

                log.info(
                    "Card found '%s' ['%s'] for '%s' ['%s-%s']: '%s,%s,%s'",
                    card_dir_basename,
                    card_id,
                    target_usbid,
                    busnum,
                    devnum,
                    info.manufacturer,
                    info.product,
                    info.version,
                )
                return AsoundCardInfo(usb_device_info=info, id_card=card_id)

            except Exception:  # pylint: disable=broad-exception-caught
                continue

        log.warning(
            "Card id not found for '%s' ['%s-%s']: '%s,%s,%s'",
            target_usbid,
            info.busnum,
            info.devnum,
            info.manufacturer,
            info.product,
            info.version,
        )
        return None
