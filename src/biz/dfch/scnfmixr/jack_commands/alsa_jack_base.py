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

"""Module for creating a JACK / ALSA source or sink bridge."""

from abc import ABC
import time

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from .jack_connection import JackConnection
from .jack_port import JackPort


class AlsaJackBase(ABC):
    """Base class for creating a JACK / ALSA source or sink.

        Attributes:
            name (str): The name of the JACK source or sink client.
            device (str): The name of the ALSA plaback device.
            channels (int): The number of channels of the ALSA device.
            rate (int): The rate in Hz of the ALSA device.
    """

    _process: Process
    _ports: list[JackPort]
    _suffix: str
    name: str
    device: str
    channels: int
    rate: int

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
        assert isinstance(channels, int)
        assert 1 <= channels
        assert isinstance(rate, int)
        assert 0 < rate

        self._process = None
        self._ports: list[JackPort] = []
        self._suffix = suffix
        self.name = name
        self.device = device
        self.channels = channels
        self.rate = rate

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

        # jack_base_name = f"{self.name}" \
        #     f"{self._JACK_PORT_INFIX}" \
        #     f"{self._suffix}"

        # while True:
        #     time.sleep(0.5)
        #     result = JackConnection.get_ports(jack_base_name)

        #     if result is None or self.channels != len(result):
        #         continue

        #     for port in result:
        #         jack_port = JackPort(port)
        #         self._ports.append(jack_port)

        #     log.info("Jack ports for '%s': %s", jack_base_name, result)
        #     break

    @property
    def is_started(self) -> bool:
        """Determines whether the process is started or not."""

        return self._process is not None and self._process.is_running

    def get_ports(self) -> list[JackPort]:
        """Retrieves all JACK ports for this bridge."""

        jack_base_name = f"{self.name}" \
            f"{self._JACK_PORT_INFIX}" \
            f"{self._suffix}"

        if any(self._ports):
            return self._ports

        while True:
            result = JackConnection.get_ports(jack_base_name)

            if result is None or self.channels != len(result):
                time.sleep(0.5)
                continue

            for port in result:
                jack_port = JackPort(port)
                self._ports.append(jack_port)

            log.info("Jack ports for '%s': %s", jack_base_name, result)
            break

        return self._ports

    # def get_ports(self) -> list[JackPort]:
    #     """Retrieves all JACK ports for this bridge."""

    #     return self._ports

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
