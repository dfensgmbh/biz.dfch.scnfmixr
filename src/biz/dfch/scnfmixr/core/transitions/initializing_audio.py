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

"""Module initialising_audio."""

from ...app import ApplicationContext
from ...mixer import AudioMixer
# from ...mixer import AudioMixerConfiguration
# from ...public.mixer import Connection, ConnectionPolicy, MixbusDevice
# from ...public.audio import AudioDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class InitializingAudio(TransitionBase):
    """Initializing the audio system."""

    _app_ctx: ApplicationContext

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.INITIALISING_AUDIO_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.INITIALISING_AUDIO_LEAVE, False),
            target_state=target)

        self._app_ctx = ApplicationContext.Factory.get()

    def invoke(self, ctx: ExecutionContext):

        assert ctx

        mixer = AudioMixer.Factory.get()
        assert mixer

        # mixbus = mixer.mixbus

        # lcl_i = mixbus.get_device(MixbusDevice.MX3)
        # ex1_i = mixbus.get_device(MixbusDevice.MX4)
        # ex2_i = mixbus.get_device(MixbusDevice.MX5)
        # lcl_o = mixbus.get_device(AudioDevice.LCL)
        # ex1_o = mixbus.get_device(AudioDevice.EX1)
        # ex2_o = mixbus.get_device(AudioDevice.EX2)

        # lcl_i.connect_to(ex1_o.as_sink_set)
        # lcl_i.connect_to(ex2_o.as_sink_set)
        # ex1_i.connect_to(lcl_o.as_sink_set)
        # ex1_i.connect_to(ex2_o.as_sink_set)
        # ex2_i.connect_to(lcl_o.as_sink_set)
        # ex2_i.connect_to(ex1_o.as_sink_set)

        # cfg = AudioMixerConfiguration().get_default()
        # cfg.default_output = Connection.sink(AudioDevice.LCL.name)

        # for obj in self._app_ctx.xputs:
        #     cfg.add_xput(obj)

        # cfg.add_connection(Connection(
        #     this=Connection.source(AudioDevice.LCL.name),
        #     other=Connection.sink(AudioDevice.EX1.name),
        # )).add_connection(Connection(
        #     this=Connection.source(AudioDevice.LCL.name),
        #     other=Connection.sink(AudioDevice.EX2.name),
        # )).add_connection(Connection(
        #     this=Connection.source(AudioDevice.EX1.name),
        #     other=Connection.sink(AudioDevice.LCL.name),
        # )).add_connection(Connection(
        #     this=Connection.source(AudioDevice.EX1.name),
        #     other=Connection.sink(AudioDevice.EX2.name),
        # )).add_connection(Connection(
        #     this=Connection.source(AudioDevice.EX2.name),
        #     other=Connection.sink(AudioDevice.LCL.name),
        # )).add_connection(Connection(
        #     this=Connection.source(AudioDevice.EX2.name),
        #     other=Connection.sink(AudioDevice.EX1.name),
        # ))

        # mixer.initialise(cfg)

        return True
