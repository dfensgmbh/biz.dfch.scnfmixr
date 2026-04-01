# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

"""Module detecting_in1."""

from biz.dfch.logging import log

from ...application_context import ApplicationContext
from ...audio import AudioDeviceInfo
from ...alsa_usb import AlsaStreamInfoParser
from ...audio import UsbAudioDeviceNotDetectedError
from ...mixer import AudioMixer
from ...mixer.jack_bus_device import JackBusDevice
from ...public.audio import AudioDevice
from ...public.mixer import AudioInput, AudioOutput
from ...public.mixer import ConnectionPolicy
from ...public.mixer import MixbusDevice
from ...public.mixer import IsoChannelDry
from ...public.mixer import IsoChannelWet
from ...public.system.messages import SystemMessage
from ...mixer import DeviceFactory
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class DetectingIn1(TransitionBase):
    """Detecting insert device IN1."""

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_IN1_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_IN1_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):

        assert isinstance(ctx, ExecutionContext)

        app_ctx = ApplicationContext.Factory.get()

        device = AudioDevice.IN1

        try:
            value = app_ctx.audio_device_map[device]
            log.debug("Detecting '%s' on '%s' ...", device, value)

            device_info = AudioDeviceInfo.Factory.create(value, max_attempts=1)
            app_ctx.audio_configuration_map[device] = device_info

            audio_input = AudioInput(device.name, device_info.source)
            audio_output = AudioOutput(device.name, device_info.sink)
            app_ctx.xputs.add(audio_input)
            app_ctx.xputs.add(audio_output)

            parser = AlsaStreamInfoParser(device_info.asound_info.card_id)
            jack_device = DeviceFactory.create_jack_alsa(
                device.name,
                device_info.asound_info.card_id,
                device_id=0,
                parser=parser
            )
            jack_device.acquire()

            mixbus = AudioMixer.Factory.get().mixbus
            for mixbus_device in mixbus.devices:
                log.warning("device: '%s'.", mixbus_device.name)
            dr1 = mixbus.get_device(MixbusDevice.DR1)
            assert isinstance(dr1, JackBusDevice), type(dr1)

            wt1 = mixbus.get_device(MixbusDevice.WT1)
            assert isinstance(wt1, JackBusDevice), wt1

            jack_device.connect_to(wt1.as_sink_set(), ConnectionPolicy.DUAL)

            dr1.sources[IsoChannelDry.MST_LEFT].connect_to(
                jack_device.sinks[2])
            dr1.sources[IsoChannelDry.MST_RIGHT].connect_to(
                jack_device.sinks[3])

            jack_device.sources[IsoChannelDry.MST_LEFT].connect_to(
                wt1.sinks[IsoChannelWet.MST_LEFT])
            jack_device.sources[IsoChannelDry.MST_RIGHT].connect_to(
                wt1.sinks[IsoChannelWet.MST_RIGHT])

            log.debug("Detecting '%s' on '%s' OK.", device, value)

            return True

        except UsbAudioDeviceNotDetectedError as ex:

            log.error("Device detection '%s' FAILED. [%s]",
                      device.name, ex)
            ctx.events.publish(SystemMessage.UiEventInfoTransitionLeaveMessage(
                UiEventInfo(
                    TransitionEvent.DETECTING_DEVICE_IN1_FAILED, False)))

            return False

        except Exception as ex:  # pylint: disable=W0718

            log.error("Device detection '%s' FAILED. [%s]",
                      device.name, ex, exc_info=True)

            return False
