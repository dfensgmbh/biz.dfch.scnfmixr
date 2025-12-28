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
    """Initializing storage."""

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
