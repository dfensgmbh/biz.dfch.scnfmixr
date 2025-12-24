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

"""Module audio_input_or_output."""

from ...jack_commands import AlsaJackBase
from ..audio import AlsaInterfaceInfo
from .input_or_output import InputOrOutput

__all__ = [
    "AudioInputOrOutput",
]


# pylint: disable=R0903
class AudioInputOrOutput(InputOrOutput):
    """Represents an audio object."""

    _alsa_jack_base: AlsaJackBase
    cfg: AlsaInterfaceInfo

    def __init__(self, name: str, cfg: AlsaInterfaceInfo):
        super().__init__()

        assert name and name.strip()
        assert cfg is not None

        self._alsa_jack_base = None

        self.name = name
        self.cfg = cfg

    @property
    def is_started(self) -> bool:
        return self._alsa_jack_base.is_started
