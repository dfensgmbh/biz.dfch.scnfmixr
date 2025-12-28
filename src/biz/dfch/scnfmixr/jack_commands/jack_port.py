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

"""Module for representing JACK ports."""

from __future__ import annotations
from dataclasses import (
    dataclass
)
from time import sleep
from typing import (
    overload,
)

from biz.dfch.logging import log
from biz.dfch.asyn import Process

from text import MultiLineTextParser

from .jack_connection import JackConnection


__all__ = [
    "JackPort"
]


@dataclass(frozen=True)
class JackPort:
    """Represents a JACK port.

    Attributes:
        name (str): The name of the JACK port.
    """

    _JACK_CONNECT_FULLNAME = "/bin/jack_connect"
    _JACK_DISCONNECT_FULLNAME = "/usr/bin/jack_disconnect"
    _JACK_LSP_FULLNAME = "/usr/bin/jack_lsp"

    name: str

    @overload
    @staticmethod
    def get_ports() -> list[JackPort]:
        ...

    @overload
    @staticmethod
    def get_ports(name: str) -> list[JackPort]:
        ...

    @staticmethod
    def get_ports(name: str | None = None) -> list[JackPort]:
        """Retrieves a list of all JACK ports."""

        result: list[JackPort] = []

        cmd: list[str] = []
        cmd.append(JackPort._JACK_LSP_FULLNAME)
        if name and name.strip():
            cmd.append(name)

        log.debug("Enumerating ports '%s' ...", name)

        result_from_process = Process.communicate(cmd, max_wait_time=3)
        text = result_from_process[0]

        visitor = JackConnection.PortVisitor()
        dic = {
            "[^\\:]+\\:\\w+": visitor.process_port,
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=3,
            dic=dic)
        parser.parse(text, is_regex=True)

        items = visitor.items
        for item in items:
            result.append(JackPort(item))

        log.info("Enumerating ports [%s] [%s].", len(items), items)

        return result

    @property
    def exists(self) -> bool:
        """Determines whether the current JACK port is active.

        Returns:
            bool: True, if the port exists; false otherwise.
        """

        result = JackConnection.get_ports(self.name)

        return (
            result is not None and
            1 == len(result)
            and self.name == result[0])

    def is_index(self, idx: int) -> bool:
        """Determines whether the port matches the specified index."""

        assert 0 < idx

        return self.name.endswith(f"_{idx}")

    def get_connections(self) -> list[JackPort]:
        """
        Retrieves the list of JACK ports currently connected to this port.

        Returns:
            list[AlsaJackBase.JackPort]: A list of JackPort instances
                representing all JACK ports that are connected to this port.
        """

        log.debug("Retrieving connections to '%s' ...", self.name)

        result = [
            JackPort(item)
            for item in JackConnection.get_connections(self.name)
        ]

        log.info("Retrieving connections to '%s' [%s] OK. %s", self.name,
                 len(result), result)

        return result

    def disconnect_all(self) -> bool:
        """Disconnects all existing connections.

        Returns:
            bool: True, if no connections to this port exist; false
                otherwise. Also True, if no connections existed before this
                call."""

        log.debug("Disconnecting all from '%s' ...", self.name)

        conns = self.get_connections()

        if conns is None or not isinstance(conns, list):
            return False
        if 0 == len(conns):
            return True

        for conn in conns:
            self.disconnect_from(conn.name)

        conns = self.get_connections()

        if conns is None or not isinstance(conns, list):
            return False
        result = 0 == len(conns)

        log.debug("Disconnecting all from '%s' %s.",
                  self.name,
                  "OK" if result else "FAILED")

        return result

    def connect_to(self, other: str) -> bool:
        """Connects this port to the specified other port.

        Args:
            other (str): Port to connect to.

        Returns:
            bool: True, if connect succeeded; false otherwise. Also returns
                True, if the connection already existed before the call.
        """

        assert other and other.strip()

        cmd: list[str] = []
        cmd.append(self._JACK_CONNECT_FULLNAME)
        cmd.append(self.name)
        cmd.append(other)

        log.debug("Connecting '%s' to '%s' ...", self.name, other)

        Process.communicate(cmd)

        conns = self.get_connections()
        if conns is None or not isinstance(conns, list):
            return False

        result = any(conn.name == other for conn in conns)

        if result:
            log.info("Connecting '%s' to '%s' OK.",
                     self.name,
                     other)
        else:
            log.error("Connecting '%s' to '%s' FAILED.",
                      self.name,
                      other)

        return result

    def disconnect_from(self, other: str) -> bool:
        """Disconnects this port from the specified other port.

        Args:
            other (str): Port to disconnect from.

        Returns:
            bool: True, if disconnect succeeded; false otherwise. Also returns
                True, if the connection did not exist before the call.
        """

        assert other and other.strip()

        cmd: list[str] = []
        cmd.append(self._JACK_DISCONNECT_FULLNAME)
        cmd.append(self.name)
        cmd.append(other)

        log.debug("Disconnecting '%s' from '%s' ...", self.name, other)

        process = Process.start(cmd, True, capture_stdout=False)
        while process.is_running:
            sleep(0.1)

        process.stop(force=True)

        conns = self.get_connections()
        if conns is None or not isinstance(conns, list):
            return False

        result = not any(conn.name == other for conn in conns)

        log.info("Disconnecting '%s' from '%s' %s.",
                 self.name,
                 other,
                 "OK" if result else "FAILED")

        return result
