# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
