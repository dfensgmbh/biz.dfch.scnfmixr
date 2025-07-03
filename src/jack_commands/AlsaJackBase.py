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

"""Module for creating a JACK / ALSA source or sink bridge."""

from abc import ABC
import time

from asyn import Process
from log import log
from .JackConnection import JackConnection
from .JackPort import JackPort


class AlsaJackBase(ABC):
    """Base class for creating a JACK / ALSA source or sink.

        Attributes:
            name (str): The name of the JACK source or sink client.
            device (str): The name of the ALSA plaback device.
            channels (int): The number of channels of the ALSA device.
            rate (int): The rate in Hz of the ALSA device.
    """

    _ZITA_A2J_BRIDGE = "/usr/bin/zita-a2j"
    _JACK_PORT_INFIX = ":"
    _ZITA_A2J_PORT_SUFFIX = "capture_"

    def __init__(self,
                 bridge: str,
                 suffix: str,
                 name: str,
                 device: str,
                 channels: int = 2,
                 rate: int = 48000
                 ) -> None:
        """Creates an instance of this class."""

        assert bridge and bridge.strip()
        assert suffix and suffix.strip()
        assert name and name.strip()
        assert device and device.strip()
        assert 1 <= channels
        assert 0 < rate

        self._ports: list[JackPort] = []
        self._suffix = suffix
        self.name = name
        self.device = device
        self.channels = channels
        self.rate = rate

        self._process = None

        cmd: list[str] = []
        cmd.append(bridge)
        cmd.append("-j")
        cmd.append(self.name)
        cmd.append("-d")
        cmd.append(self.device)
        cmd.append("-c")
        cmd.append(self.channels)
        cmd.append("-r")
        cmd.append(self.rate)

        log.debug("Starting '%s' ...", cmd)

        self._process = Process.start(cmd, False)

        log.info("Started '%s' [pid=%s] [is_running=%s] ...",
                 cmd,
                 self._process.pid,
                 self._process.is_running)

        jack_base_name = f"{self.name}" \
            f"{self._JACK_PORT_INFIX}" \
            f"{self._suffix}"

        while True:
            time.sleep(0.5)
            result = JackConnection.get_ports(jack_base_name)

            if result is None or self.channels != len(result):
                continue

            for port in result:
                jack_port = JackPort(port)
                self._ports.append(jack_port)

            log.info("Jack ports for '%s': %s", jack_base_name, result)
            break

    def get_ports(self) -> list[JackPort]:
        """Retrieves all JACK ports for this bridge."""

        return self._ports

    def get_port_names(self) -> list[str]:
        """Retrieves all JACK port names.

        Returns:
            list(str): The list of port names associated with this bridge.
        """

        result: list[str] = []

        for i in range(0, self.channels, 1):
            jack_name = f"{self.name}" \
                f"{self._JACK_PORT_INFIX}" \
                f"{self._suffix}" \
                f"{i}"
            result.append(jack_name)

        return result

    def stop(self) -> None:
        """Stops the ALSA to JACK bridge.

        Returns:
            None:
        """

        log.debug("Stopping '%s' [device=%s] [%s, %s] ...",
                  self.name,
                  self.device,
                  self.channels,
                  self.rate)

        if self._process is None or not self._process.is_running:
            return

        self._process.stop(force=True)
        self._process = None
