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

"""Module initialising_storage."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.storage import DeviceOperations
from ...public.storage import StorageDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class FormattingStorage(TransitionBase):
    """Initialising storage."""

    _device: StorageDevice

    def __init__(self, event: str, target: StateBase, device: StorageDevice):
        """Default ctor."""

        assert isinstance(event, str) and event.strip()
        assert isinstance(target, StateBase)
        assert isinstance(device, StorageDevice)

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.FORMATTING_STORAGE_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.FORMATTING_STORAGE_LEAVE, False),
            target_state=target)

        self._device = device

    def invoke(self, _) -> bool:

        result = False

        app_ctx = ApplicationContext.Factory.get()

        addr = app_ctx.storage_device_map.get(self._device, None)
        if addr is None:
            log.debug("Device '%s' not specified. Skipping ...",
                      self._device.name)
            return result

        device_info = app_ctx.storage_configuration_map.get(self._device, None)
        if device_info is None:
            log.debug("Device '%s' not configured. Skipping ...",
                      self._device.name)
            return result

        op = DeviceOperations(device_info)

        if op.is_mounted:

            result = op.unmount()
            if not result:
                log.error("Unmounting storage device '%s' FAILED.",
                          self._device.name)
                return result

            log.info("Unmounting storage device '%s' OK.",
                     self._device.name)

        result = op.format_disk(self._device.name)
        if not result:
            log.error("Formatting storage device '%s' FAILED.",
                      self._device.name)

        log.info("Formatting storage device '%s' OK.",
                 self._device.name)

        result = op.mount()
        if not result:
            log.error("Mounting storage device '%s' FAILED.",
                      self._device.name)

        log.info("Mounting storage device '%s' OK.",
                 self._device.name)

        return result


class FormattingStorageRc1(FormattingStorage):
    """Formatting storage RC1."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            target,
            StorageDevice.RC1,
        )


class FormattingStorageRc2(FormattingStorage):
    """Formatting storage RC2."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            target,
            StorageDevice.RC2,
        )
