# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""Tests for signal_point."""

from biz.dfch.logging import log
from biz.dfch.scnfmixr.jack_commands import JackPort


class MockAlsaJackBase:
    """MockAlsaJackBase."""
    name: str
    device: str
    channels: int
    rate: int

    def __init__(self, name: str, device: str, channels: int = 2,
                 rate: int = 48000):
        self.name = name
        self.device = device
        self.channels = channels
        self.rate = rate

    def stop(self):
        """stop"""
        log.debug("Stopping '%s' [device=%s] [%s, %s] ...",
                  self.name,
                  self.device,
                  self.channels,
                  self.rate)

    def get_ports(self) -> list[JackPort]:
        """get_ports"""

        result = []

        for i in range(0, self.channels):

            result.append(JackPort(f"{self.name}:{i+1}"))

        return result

    def get_port_names(self) -> list[str]:
        """get_port_names"""

        result = []

        for i in range(0, self.channels):

            result.append(f"{self.name}:{i+1}")

        return result


class MockJackToAlsa(MockAlsaJackBase):
    """MockJackToAlsa."""

    def get_ports(self) -> list[JackPort]:
        result = [JackPort(
            e.replace(f"{self.name}:", f"{self.name}:playback_"))
            for e in super().get_port_names()]

        log.debug("get_ports '%s': [%s]", self.name, result)

        return result

    def get_port_names(self) -> list[str]:
        result = [
            e.replace(f"{self.name}:", f"{self.name}:playback_")
            for e in super().get_port_names()]

        log.debug("get_port_names '%s': [%s]", self.name, result)

        return result


class MockAlsaToJack(MockAlsaJackBase):
    """MockAlsaToJack."""

    def get_ports(self) -> list[JackPort]:
        result = [JackPort(
            e.replace(f"{self.name}:", f"{self.name}:capture_"))
            for e in super().get_port_names()]

        log.debug("get_ports '%s': [%s]", self.name, result)

        return result

    def get_port_names(self) -> list[str]:
        result = [
            e.replace(f"{self.name}:", f"{self.name}:capture_")
            for e in super().get_port_names()]

        log.debug("get_port_names '%s': [%s]", self.name, result)

        return result
