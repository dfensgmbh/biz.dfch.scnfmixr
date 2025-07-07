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

"""Module detecting_hi1."""

from biz.dfch.asyn import ConcurrentQueueT
from biz.dfch.logging import log

from ...app import ApplicationContext
from ...hi_devices import HiDevices
from ...ui import UiEventInfo
from ...ui import TransitionBase
from ...ui import StateBase
from ...ui.keyboard import DetectingHi1Worker
from ...ui.keyboard import KeyboardHandler
from ..transition_event import TransitionEvent


class DetectingHi1(TransitionBase):
    """Detecting device HI1."""

    _handler: KeyboardHandler

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI1_LEAVE, False),
            target_state=target)

        self._handler = None

    def invoke(self, ctx):

        value = ApplicationContext().input_device_map[HiDevices.HI1]
        worker = DetectingHi1Worker(value)
        device = worker.select()

        if device is None or "" == device.strip():
            log.error("No input device for at: '%s'", value)
            return False

        log.debug("Input device found: '%s'", device)

        self._handler = KeyboardHandler(ctx.events, device)
        log.debug("Starting keyboard processing ...")
        self._handler.start()

        return True
