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

"""Module detecting_rc1."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.storage import DetectingRcWorker
from ...public.storage import StorageDevice
from ...public.system.messages import SystemMessage
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class DetectingRc1(TransitionBase):
    """Detecting device RC1."""

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_RC1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_RC1_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):

        assert isinstance(ctx, ExecutionContext)

        device = StorageDevice.RC1

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.storage_device_map[device]

        log.info("Detecting storage device '%s' at '%s'...",
                 device.name, value)

        selector = DetectingRcWorker(device, value)
        result = selector.select()

        if result is None:
            ctx.events.publish(SystemMessage.UiEventInfoTransitionLeaveMessage(
                UiEventInfo(
                    TransitionEvent.DETECTING_DEVICE_RC1_FAILED, False)))
            return False

        log.debug("Detected storage device '%s': %s",
                  device.name, result)

        return True
