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

from biz.dfch.logging import log
from biz.dfch.asyn import Process

__all__ = [
    "Playback",
]


class Playback:
    """Sends audio to an ALSA device."""

    _APLAY_FULLNAME = "/bin/aplay"

    def __init__(self, device: str, name: str, wait_on_completion: bool = False):
        """Plays an audio file to the specified device.
        Args:
            device (str): An ALSA device string, e.g. `hw:1`, `plughw:1,0`, `hw:CARD=ABC`, `hw:CARD=ABC,DEV=1`
            name (str): The full path and name to an audio file.
            wait_on_completion (bool): If `True`, waits until the audio has finished playing. \
            `False` otherwise (*default*).
        Returns:
            Returns an instance to this class.
        Raises:
            FileNotFoundError: If the specified audio file `name` cannot be found, \
            a `FileNotFoundError` will be thrown.
        """

        assert device is not None and "" == device.strip()
        assert name is not None and "" == name.strip()

        self._device = device
        self._name = name

        args = [self._APLAY_FULLNAME, "-D", device, name]

        self._process = Process.start(args, wait_on_completion=wait_on_completion)

    @property
    def process(self) -> Process:
        return self._process
