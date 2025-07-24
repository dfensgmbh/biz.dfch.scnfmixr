# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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
