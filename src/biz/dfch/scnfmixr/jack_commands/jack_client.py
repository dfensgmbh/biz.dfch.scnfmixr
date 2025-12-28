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

"""Module jack_client."""

from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field

from biz.dfch.scnfmixr.jack_commands.jack_port import JackPort


__all__ = [
    "JackPort"
]


@dataclass(frozen=True)
class JackClient:
    """Represents a JACK client."""

    name: str
    ports: frozenset[JackPort] = field(default_factory=frozenset)

    @staticmethod
    def get() -> set[JackClient]:
        """Retrieves all currently existing JACK clients.

        Return:
            set[JackClient]: A set of JACK clients.
        """

        dic: dict[str, set[JackPort]] = defaultdict(set)
        result: set[JackClient] = set()

        ports = JackPort.get_ports()
        for port in ports:
            name, _ = port.name.split(":", 1)

            dic[name].add(port)

        for name, ports in dic.items():
            client = JackClient(name, frozenset(ports))
            result.add(client)

        return result
