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

"""Module detecting_hi2."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...devices.keyboard import DetectingHi2Worker
from ...public.input import InputDevice
from ...ui import StreamdeckHandler

from ..fsm import UiEventInfo
from ..fsm import StateBase
from ..fsm import TransitionBase
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class DetectingHi2(TransitionBase):
    """Detecting device HI2."""

    _handler: StreamdeckHandler

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI2_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI2_LEAVE, False),
            target_state=target)

        self._handler = None

    def invoke(self, ctx):

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.input_device_map[InputDevice.HI2]
        worker = DetectingHi2Worker(value)
        device = worker.select()

        if device is None or "" == device.strip():
            log.error("No input device detected at: '%s'.", value)
            return False

        log.debug("Input device detected at: '%s'", device)

        self._handler = StreamdeckHandler(device)
        log.debug("Starting Streamdeck processing ...")
        result = self._handler.start()
        if result:
            log.info("Starting Streamdeck processing SUCCEEDED.")
        else:
            log.error("Starting Streamdeck processing FAILED.")

        return result
