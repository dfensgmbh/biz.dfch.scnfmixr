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

    def invoke(self):
        return super().invoke()
