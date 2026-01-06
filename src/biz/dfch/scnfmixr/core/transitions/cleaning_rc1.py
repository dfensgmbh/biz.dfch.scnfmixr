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

"""Module cleaning_rc1."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.storage import DeviceOperations
from ...public.storage import StorageDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class CleaningRc1(TransitionBase):
    """Cleaning device RC1."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.CLEANING_DEVICE_RC1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.CLEANING_DEVICE_RC1_LEAVE, False),
            target_state=target)

    def invoke(self, _):

        device = StorageDevice.RC1

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.storage_device_map[device]

        log.debug("Cleaning storage device '%s' at '%s'...",
                  device.name, value)

        device_info = app_ctx.storage_configuration_map.get(
            device, None)

        result = False if device_info is None else DeviceOperations(
            device_info).clean()

        if result:
            log.info("Cleaning storage device '%s' OK.",
                     device.name)
        else:
            log.error("Cleaning storage device '%s' FAILED.",
                      device.name)

        return result
