# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Module detecting_hi1."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.keyboard import DetectingHi1Worker
from ...public.input import InputDevice
from ...ui import KeyboardHandler

from ..fsm import UiEventInfo
from ..fsm import StateBase
from ..fsm import TransitionBase
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class DetectingHi1(TransitionBase):
    """Detecting device HI1."""

    _handler: KeyboardHandler

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI1_LEAVE, False),
            target_state=target)

        self._handler = None

    def invoke(self, ctx):

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.input_device_map[InputDevice.HI1]
        worker = DetectingHi1Worker(value)
        device = worker.select()

        if device is None or "" == device.strip():
            log.error("No input device detected at: '%s'.", value)
            return False

        log.debug("Input device detected at: '%s'", device)

        event_map_type = app_ctx.ui_parameters.menu_profile.get_event_map(
            InputDevice.HI1)
        assert event_map_type is not None
        event_map = event_map_type()

        self._handler = KeyboardHandler(device, event_map)
        log.debug("Starting keyboard processing ...")
        result = self._handler.start()
        if result:
            log.info("Starting keyboard processing SUCCEEDED.")
        else:
            log.error("Starting keyboard processing FAILED.")

        return result
