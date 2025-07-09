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

"""Module detecting_rc_wroker_base."""

from ..interface_detector_base import InterfaceDetectorBase


class DetectingRcWorkerBase(InterfaceDetectorBase):
    """Base class for detecting storage devices."""

    _UDEVADM_FULLNAME = "/usr/bin/udevadm"
    _UDEVADM_OPTION_INFO = "info"
    _UDEVADM_OPTION_ALL = "-a"
    _UDEVADM_OPTION_NOP_PAGER = "--no-pager"
    _UDEVADM_OPTION_NAME = "--name"

    _DEV_INPUT_PATH: str = "/dev/"
    _DEV_INPUT_EVENT_PREFIX: str = "sd"
    _DEV_INPUT_EVENT_PATH_GLOB: str = (
        _DEV_INPUT_PATH + _DEV_INPUT_EVENT_PREFIX + "*")

    _value: str
    _event_device_candidates: list[str]

    def __init__(self, value: str):
        super().__init__()

        assert value and value.strip()

        self._value = value

        self._event_device_candidates = []
