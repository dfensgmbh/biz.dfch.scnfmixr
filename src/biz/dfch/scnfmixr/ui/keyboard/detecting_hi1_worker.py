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

"""Module detecting_h1_worker."""

import glob
import os

from text import MultiLineTextParser
from biz.dfch.asyn import Process
from biz.dfch.logging import log
from .input_event_device_visitor import InputEventDeviceVisitor
from .interface_detector_base import InterfaceDetectorBase


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

        for candidate in glob.glob(self._DEV_INPUT_EVENT_PATH_GLOB):

            cmd: list[str] = [
                self._UDEVADM_FULLNAME,
                self._UDEVADM_OPTION_INFO,
                candidate,
            ]

            process = Process.start(
                cmd, wait_on_completion=True, capture_stdout=True)

            text = process.stdout

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
