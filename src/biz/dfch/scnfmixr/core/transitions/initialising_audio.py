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

"""Module initialising_audio."""

from ...app import ApplicationContext
from ...mixer import AudioMixer
from ...mixer import AudioMixerConfiguration
from ...public.mixer import Connection
from ...public.audio import AudioDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class InitialisingAudio(TransitionBase):
    """Initialising the audio system."""

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

        cfg = AudioMixerConfiguration().get_default()
        cfg.default_output = Connection.sink(AudioDevice.LCL.name)

        for obj in self._app_ctx.xputs:
            cfg.add_xput(obj)

        cfg.add_connection(Connection(
            this=Connection.source(AudioDevice.LCL.name),
            other=Connection.sink(AudioDevice.EX1.name),
        )).add_connection(Connection(
            this=Connection.source(AudioDevice.LCL.name),
            other=Connection.sink(AudioDevice.EX2.name),
        )).add_connection(Connection(
            this=Connection.source(AudioDevice.EX1.name),
            other=Connection.sink(AudioDevice.LCL.name),
        )).add_connection(Connection(
            this=Connection.source(AudioDevice.EX1.name),
            other=Connection.sink(AudioDevice.EX2.name),
        )).add_connection(Connection(
            this=Connection.source(AudioDevice.EX2.name),
            other=Connection.sink(AudioDevice.LCL.name),
        )).add_connection(Connection(
            this=Connection.source(AudioDevice.EX2.name),
            other=Connection.sink(AudioDevice.EX1.name),
        ))

        mixer.initialise(cfg)

        return True
