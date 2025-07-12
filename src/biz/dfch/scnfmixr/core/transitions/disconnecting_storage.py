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

"""Module unmounting_storage."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.storage import DeviceOperations
from ...public.storage import StorageDevice
from ...ui import UiEventInfo
from ...ui import TransitionBase
from ...ui import StateBase
from ..transition_event import TransitionEvent


class DisconnectingStorage(TransitionBase):
    """Unmounting storage."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DISCONNECTING_STORAGE_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DISCONNECTING_STORAGE_LEAVE, False),
            target_state=target)

    def invoke(self, _) -> bool:

        result = True

        app_ctx = ApplicationContext.Factory.get()

        for device in StorageDevice:

            addr = app_ctx.storage_device_map.get(device, None)
            if addr is None:
                log.debug("Device '%s' not specified. Skipping ...",
                          device.name)
                continue

            device_info = app_ctx.storage_configuration_map.get(device, None)
            if device_info is None:
                log.debug("Device '%s' not configured. Skipping ...",
                          device.name)
                continue

            op = DeviceOperations(device_info)

            if op.is_mounted:

                result = result and op.unmount()
                if result:
                    log.info("Unmounting storage device '%s' SUCCEEDED.",
                             device.name)
                else:
                    log.error("Unmounting storage device '%s' FAILED.",
                              device.name)
                    continue

            result = result and op.poweroff()
            if result:
                log.info("Powering off storage device '%s' SUCCEEDED.",
                         device.name)
            else:
                log.error("Powering off storage device '%s' FAILED.",
                          device.name)

        return result
