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

"""Module detecting_rc_worker_base."""

from __future__ import annotations
import json

from biz.dfch.logging import log
from biz.dfch.asyn import Process

from ..interface_detector_base import InterfaceDetectorBase
from ...public.storage.storage_device_info import StorageDeviceInfo
from ...public.storage.block_device_type import BlockDeviceType


class DetectingRcWorkerBase(InterfaceDetectorBase):
    """Base class for detecting storage devices."""

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

    _DEV_INPUT_PATH: str = "/dev/"
    _DEV_STORAGE_PREFIX: str = "sd"
    _DEV_STORAGE_PATH_GLOB: str = (
        _DEV_INPUT_PATH + _DEV_STORAGE_PREFIX + "*")

    _value: str
    _event_device_candidates: list[str]

    def __init__(self, value: str):
        super().__init__()

        assert value and value.strip()

        self._value = value

        self._event_device_candidates = []

    def _get_removable_devices(self) -> list[StorageDeviceInfo]:

        result: list[DetectingRcWorkerBase.StorageDeviceInfo] = []

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
                        f"{self._DEV_INPUT_PATH}"
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
