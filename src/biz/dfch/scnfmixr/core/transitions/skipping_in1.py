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

"""Module skipping_in1."""

from biz.dfch.logging import log

from ...mixer import AudioMixer
from ...mixer.jack_bus_device import JackBusDevice
from ...public.mixer import ConnectionPolicy
from ...public.mixer import MixbusDevice

from ..fsm import StateBase, TransitionBase
from ..fsm import UiEventInfo
from ..transition_event import TransitionEvent


class SkippingIn1(TransitionBase):
    """Skips IN1 insert device initialization."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.SKIPPING_DEVICE_IN1_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):

        mixbus = AudioMixer.Factory.get().mixbus
        for mixbus_device in mixbus.devices:
            log.warning("device: '%s'.", mixbus_device.name)
        dr1 = mixbus.get_device(MixbusDevice.DR1)
        assert isinstance(dr1, JackBusDevice), type(dr1)
        wt1 = mixbus.get_device(MixbusDevice.WT1)
        assert isinstance(wt1, JackBusDevice), wt1
        dr1.connect_to(wt1.as_sink_set(), ConnectionPolicy.DUAL)

        return True
