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

"""Module detecting_lcl."""

import time

from biz.dfch.logging import log

from ...alsa_usb import AlsaStreamInfoParser
from ...application_context import ApplicationContext
from ...audio import AudioDeviceInfo
from ...audio import UsbAudioDeviceNotDetectedError
from ...jack_commands import JackConnection
from ...mixer import AudioMixer
from ...mixer import DeviceFactory
from ...public.audio import AudioDevice
from ...public.mixer import AudioInput, AudioOutput
from ...public.mixer import ConnectionPolicy
from ...public.mixer import MixbusDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class DetectingLcl(TransitionBase):  # pylint: disable=R0903
    """Detecting device LCL."""

    def __init__(self, event: str, target_state: StateBase):

        assert event and event.strip()
        assert target_state

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_LCL_LEAVE, False),
            target_state=target_state)

    def invoke(self, _):

        app_ctx = ApplicationContext.Factory.get()

        device = AudioDevice.LCL

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
            channel = mixbus.get_device(MixbusDevice.DR0)
            jack_device.connect_to(channel.as_sink_set(), ConnectionPolicy.DUAL)
            bus = mixbus.get_device(MixbusDevice.MX3)
            bus.connect_to(jack_device.as_sink_set(), ConnectionPolicy.DUAL)

            # Here, we wait until we see the zita device running.
            for sink in jack_device.sinks:

                log.debug("Waiting for sink '%s' ...", sink.name)
                while not JackConnection.has_port_name(sink.name):
                    time.sleep(0.25)
                log.info("Waiting for sink '%s' OK.", sink.name)

                log.debug("Waiting for sink '%s' ...", sink.name)
                while not JackConnection.has_port_name(sink.name):
                    time.sleep(0.25)
                log.info("Waiting for sink '%s' OK.", sink.name)

            log.debug("Detecting '%s' on '%s' OK.", device, value)

            return True

        except UsbAudioDeviceNotDetectedError as ex:

            log.error("Device detection '%s' FAILED. [%s]",
                      device.name, ex)

            return False

        except Exception as ex:  # pylint: disable=W0718

            log.error("Device detection '%s' FAILED. [%s]",
                      device.name, ex, exc_info=True)

            return False
