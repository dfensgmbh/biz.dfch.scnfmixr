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

"""Module audio_output."""

from ...jack_commands import JackToAlsa

from ..audio import AlsaInterfaceInfo
from ..audio import Constant
from .audio_input_or_output import AudioInputOrOutput
from .connection import Connection
from .output import Output

__all__ = [
    "AudioOutput",
]


# pylint: disable=R0903
class AudioOutput(AudioInputOrOutput, Output):
    """Represents an audio output."""

    def __init__(self, name: str, cfg: AlsaInterfaceInfo):
        super().__init__(
            Connection.sink(name),
            cfg)

    def start(self) -> bool:

        self._alsa_jack_base = JackToAlsa(
            name=self.name,
            device=Constant.get_raw_device_name(
                self.cfg.card_id, self.cfg.interface_id
            ),
            channels=self.cfg.channel_count,
            rate=self.cfg.sample_rate.value)

        return self._alsa_jack_base.is_started

    def stop(self) -> bool:

        self._alsa_jack_base.stop()

        return not self._alsa_jack_base.is_started

    def connect_to(self, other) -> bool:
        ...

    def invoke(self):
        raise NotImplementedError

