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
