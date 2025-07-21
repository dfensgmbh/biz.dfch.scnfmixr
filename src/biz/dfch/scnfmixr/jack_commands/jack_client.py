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
