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

"""Module detecting_h1_worker."""

import glob

from text import MultiLineTextParser
from biz.dfch.asyn import Process
from biz.dfch.logging import log
from .input_event_device_visitor import InputEventDeviceVisitor
from ..interface_detector_base import InterfaceDetectorBase


class DetectingHi1Worker(InterfaceDetectorBase):
    """Implements the logic from `DetectingHi`."""

    _UDEVADM_FULLNAME = "/usr/bin/udevadm"
    _UDEVADM_OPTION_INFO = "info"
    _DEV_INPUT_PATH: str = "/dev/input/"
    _DEV_INPUT_EVENT_PREFIX: str = "event"
    _DEV_INPUT_EVENT_PATH_GLOB: str = (
        _DEV_INPUT_PATH + _DEV_INPUT_EVENT_PREFIX + "*")

    _value: str
    _event_device_candidates: list[str]

    def __init__(self, value: str):
        super().__init__()

        assert value and value.strip()

        self._value = f"/{value}"

        self._event_device_candidates = []

    def select(self) -> str:
        """Selects a matching interface and returns it device path.

        Returns
            str: The device path of an HID input event device that matches the
                value specified in the ctor call.
        """

        # Note: as it seems, the input device is always "event5". So, process
        # it first, to speed things up in test.
        candidates = sorted(glob.glob(self._DEV_INPUT_EVENT_PATH_GLOB),
                            key=lambda e: (len(e), e))
        device = next((e for e in candidates if e.endswith("event5")), None)
        if device:
            candidates.remove(device)
            candidates.insert(0, device)

        for candidate in candidates:

            cmd: list[str] = [
                self._UDEVADM_FULLNAME,
                self._UDEVADM_OPTION_INFO,
                candidate,
            ]

            text, _ = Process.communicate(cmd)

            visitor = InputEventDeviceVisitor()

            # Example output from udevadm.
            # user@host:~ $ udevadm info /dev/input/event5
            # E: DEVPATH=/devices/platform/axi/1000120000.pcie/1f00300000.usb/
            #   xhci-hcd.1/usb3/3-1/3-1.4/3-1.4:1.0/0003:276D:FFE3.0008/
            #       input/input16/event5
            # E: DEVNAME=/dev/input/event5
            # E: ID_INPUT_KEYBOARD=1

            dic = {
                "E: DEVPATH=": visitor.process_devpath,
                "E: DEVNAME=": visitor.process_devname,
                "E: ID_INPUT_KEYBOARD=": visitor.process_id_input_keyboard,
            }

            parser = MultiLineTextParser(
                indent=" ",
                length=3,
                dic=dic)
            parser.parse(text)

            result = visitor.result

            log.debug(result)
            if not (
                result.device_name
                and result.device_path
                and self._value in result.device_path
                and result.is_input
            ):
                continue

            return result.device_name

        return None
