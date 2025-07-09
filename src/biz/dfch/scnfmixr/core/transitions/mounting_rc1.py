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

"""Module mounting_rc1."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...public.storage.rc_devices import RcDevices
from ...ui import UiEventInfo
from ...ui import TransitionBase
from ...ui import StateBase
from ..transition_event import TransitionEvent
from ...devices.storage import DeviceOperations


class MountingRc1(TransitionBase):
    """Mounting RC1."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_RC1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_RC1_LEAVE, False),
            target_state=target)

    def invoke(self, _):

        app_ctx = ApplicationContext()

        value = app_ctx.storage_device_map[RcDevices.RC1]

        log.debug("Mounting storage device '%s' at '%s'...",
                  RcDevices.RC1.name, value)

        device: str = "/dev/sda1"
        mount_point: str = "/mnt/rc1"
        result = DeviceOperations.mount(device, mount_point)

        if result:
            log.info("Mounting storage device '%s' SUCCEEDED.",
                     RcDevices.RC1.name)
        else:
            log.error("Mounting storage device '%s' FAILED.",
                      RcDevices.RC1.name)

        return result
