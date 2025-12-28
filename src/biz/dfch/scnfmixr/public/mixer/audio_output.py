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
