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

"""Module for creating an ALSA to JACK bridge."""

from .alsa_jack_base import AlsaJackBase


class AlsaToJack(AlsaJackBase):
    """Creates an ALSA to JACK source.

        Attributes:
            name (str): The name of the JACK source client.
            device (str): The name of the ALSA capture device.
            channels (int): The number of channels of the ALSA device.
            rate (int): The rate in Hz of the ALSA device.
    """

    _ZITA_BRIDGE = "/usr/bin/zita-a2j"
    _ZITA_PORT_SUFFIX = "capture_"

    def __init__(self, name: str, device: str, channels: int = 2,
                 rate: int = 48000):
        """Creates an instance of this class."""

        super().__init__(
            self._ZITA_BRIDGE,
            self._ZITA_PORT_SUFFIX,
            name,
            device,
            channels,
            rate)
