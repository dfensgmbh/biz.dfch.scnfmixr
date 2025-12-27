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

"""Module detecting_hi1."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...public.input import InputDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ...devices.keyboard import DetectingHi1Worker
from ...ui import KeyboardHandler
from ..transition_event import TransitionEvent


# pylint: disable=R0903
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

        app_ctx = ApplicationContext.Factory.get()

        value = app_ctx.input_device_map[InputDevice.HI1]
        worker = DetectingHi1Worker(value)
        device = worker.select()

        if device is None or "" == device.strip():
            log.error("No input device detected at: '%s'", value)
            return False

        log.debug("Input device detected at: '%s'", device)

        self._handler = KeyboardHandler(device)
        log.debug("Starting keyboard processing ...")
        result = self._handler.start()
        if result:
            log.info("Starting keyboard processing SUCCEEDED.")
        else:
            log.error("Starting keyboard processing FAILED.")

        return result
