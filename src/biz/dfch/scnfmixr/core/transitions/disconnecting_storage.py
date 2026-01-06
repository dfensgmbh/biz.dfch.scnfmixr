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

"""Module unmounting_storage."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.storage import DeviceOperations
from ...public.storage import StorageDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
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
        result = DisconnectingStorage.disconnect()

        return result

    @staticmethod
    def disconnect() -> bool:
        """Disconnects and powers off any connected storage devices."""

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
                    log.info("Unmounting storage device '%s' OK.",
                             device.name)
                else:
                    log.error("Unmounting storage device '%s' FAILED.",
                              device.name)
                    continue

            result = result and op.poweroff()
            if result:
                log.info("Powering off storage device '%s' OK.",
                         device.name)
            else:
                log.error("Powering off storage device '%s' FAILED.",
                          device.name)

        return result
