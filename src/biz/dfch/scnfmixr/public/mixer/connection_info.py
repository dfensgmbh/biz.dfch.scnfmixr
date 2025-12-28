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

"""Module connection_info."""


__all__ = [
    "ConnectionInfo",
]


class ConnectionInfo:
    """Information about JACK clients and conections.

    Each key holds an entry in the form `client:port` with port `text_number`.
    Optionally, the `client` segment can have additional '`:`'.

    * `system:capture_1` (starting at  '`1`')
    * `system:playback_1`
    * `arbi-tra_ry:text_42`
    * `prefix:infix:port_1`
    * `abcd:efgh:ijkl_1`

    The format of the items in the value of a key have the same format.
    """

    _SEPARATOR = ':'

    _values: dict[tuple[str, bool], list[str]]

    IDX_CLIENT = 0
    IDX_PORT = 1
    IDX_SOURCE = 0
    IDX_NAME = 0
    IDX_TYPE = 1

    def __init__(self, values: dict[tuple[str, bool], list[str]]):

        assert isinstance(values, dict)

        for entry, others in values.items():
            assert isinstance(entry, tuple) and 2 == len(entry)
            assert isinstance(entry[self.IDX_SOURCE], str)
            assert self._SEPARATOR in entry[self.IDX_SOURCE]
            assert isinstance(entry[self.IDX_TYPE], bool)
            assert isinstance(others, list)
            for other in others:
                assert isinstance(other, str)

        self._values = values
        self._values = self.clone()

    @staticmethod
    def to_entry(client: str, port: str) -> str:
        """Returns the full JACK name.

        * `'system', 'capture_1' -- > 'system:capture_1'`
        * `'Alsa:LCL-I', 'playback_2' -- > 'Alsa:LCL-I:playback_2'`

        Args:
            client (str): The client segment of the JACK name.
            port (str): The port segment of the JACK name.

        Returns:
            str: The full JACK name.
        """

        assert isinstance(client, str) and client.strip()
        assert isinstance(port, str) and port.strip()

        return f"{client}{ConnectionInfo._SEPARATOR}{port}"

    @staticmethod
    def from_entry(value: str) -> tuple[str, str]:
        """Splits a full JACK name into client and port.

        * `'system:capture_1' -- > ('system', 'capture_1')`
        * `'Alsa:LCL-I:playback_2' -- > ('Alsa:LCL-I', 'playback_2')`

        Args:
            value (str): The full JACK name.

        Returns:
            tuple (str, str): Client and port segment of the JACK name.
        """

        client, port = value.rsplit(ConnectionInfo._SEPARATOR, 1)

        result = (client, port)

        return result

    @property
    def all(self) -> list[tuple[str, str]]:
        """Returns a list of connection entries.

        Returns:
            list (tuple[str, str]): A list of tuples containing source and sink.
        """

        result: set[tuple[str, str]] = set()

        for entry_type, others in self._values.items():
            entry, is_sink = entry_type
            for other in others:
                if is_sink:
                    result.add((other, entry))
                else:
                    result.add((entry, other))

        return list(result)

    @property
    def clients(self) -> dict[str, list[tuple[str, str]]]:
        """Returns connecections grouped by client names.

        * `'system'`
            * `'system:capture_1' : 'system:playback_1'`
            * `'system:capture_2' : 'system:playback_2'`

        Returns:
            dict (str, list[tuple[str, str]]): Keys contain client names; each
                value list tuple contains source/sink names.
        """

        result: dict[str, list[str]] = {}

        for entry_type, others in self._values.items():
            entry, is_sink = entry_type
            client, _ = ConnectionInfo.from_entry(entry)

            if client not in result:
                result[client] = []

            for other in others:
                if is_sink:
                    result[client].append((other, entry))
                else:
                    result[client].append((entry, other))

        return [(k, v) for k, v in result.items() if 0 < len(v)]

    @property
    def sources(self) -> list[str]:
        """Returns sources."""
        return [e[self.IDX_NAME]
                for e in self._values.keys() if not e[self.IDX_TYPE]]

    def get_sources(self, value: str) -> list[str]:
        """Returns sources of specified client (eg. **`system`**)."""

        assert isinstance(value, str) and value.strip()

        return [e[self.IDX_NAME]
                for e in self._values.keys()
                if not e[self.IDX_TYPE]
                and ConnectionInfo.from_entry(
                    e[self.IDX_CLIENT])[self.IDX_CLIENT] == value]

    @property
    def sinks(self) -> list[str]:
        """Returns sinks."""
        return [e[self.IDX_NAME]
                for e in self._values.keys() if e[self.IDX_TYPE]]

    def get_sinks(self, value: str) -> list[str]:
        """Returns sinks of specified client (eg. **`system`**)."""

        assert isinstance(value, str) and value.strip()

        return [e[self.IDX_NAME]
                for e in self._values.keys()
                if e[self.IDX_TYPE]
                and ConnectionInfo.from_entry(
                    e[self.IDX_CLIENT])[self.IDX_CLIENT] == value]

    def is_client(self, value: str) -> bool:
        """Determines wheter the specified client name (**`system`**) exists.

        Args:
            value (str): The client name to match.

        Returns:
            bool: True, if the client could be found; false, otherwise.
        """

        assert isinstance(value, str) and value.strip()

        return any(
            ConnectionInfo.from_entry(
                e[self.IDX_NAME])[self.IDX_CLIENT] == value
            for e in self._values)

    def is_entry(self, value: str) -> bool:
        """Determines wheter the specified entry name (**`system:capture_1`**)
        exists.

        Args:
            value (str): The entry name to match.

        Returns:
            bool: True, if the entry could be found; false, otherwise.
        """

        assert isinstance(value, str) and value.strip()

        return any(e[self.IDX_NAME] == value for e in self._values.keys())

    def is_source(self, value: str) -> bool:
        """Determines wheter the specified entry name (**`system:capture_1`**)
        is a source.

        Args:
            value (str): The entry name to match.

        Returns:
            bool: True, if the entry is a source; false, otherwise.
        """

        assert isinstance(value, str) and value.strip()

        return any(e[self.IDX_NAME] == value
                   and not e[self.IDX_TYPE]
                   for e in self._values.keys())

    def is_sink(self, value: str) -> bool:
        """Determines wheter the specified entry name (**`system:capture_1`**)
        is a sink.

        Args:
            value (str): The entry name to match.

        Returns:
            bool: True, if the entry is a sink; false, otherwise.
        """

        assert isinstance(value, str) and value.strip()

        return any(e[self.IDX_NAME] == value
                   and e[self.IDX_TYPE]
                   for e in self._values.keys())

    def has_connections(self, client: str) -> bool:
        """Determines whether the specified client name (**`system`**) has
        connections.

        Returns:
            bool: True, if the client has connection; false, otherwise.
        """

        return 0 < len(self.get_connections(client))

    def get_connections(
            self,
            client: str,
    ) -> list[tuple[str, str]]:
        """Gets connections of the specified client name (**`system`**).

        Args:
            client (str): The name of the client for which connections will be
                returned.

        Returns:
            list (tuple[str, str]): A list of tuples containing both ends of
                the connection. First item is associated with client.
        """

        assert isinstance(client, str) and client.strip()

        if not self.is_client(client):
            return []

        result = self._group_by_client()[client]
        return result

    def get_connection_entries(self, entry: str) -> list[str]:
        """Returns the connections entries for this entry name
        (**`system:capture_1`**).

        Args:
            entry (str): The entry name to match.

        Returns:
            list[str]: A list of entries this `entry` is connected to.
        """

        assert isinstance(entry, str) and entry.strip()

        if not self.is_entry(entry):
            result: list[str] = []
            return result

        # Check either key combination, or default.
        return self._values.get((entry, False),
                                self._values.get((entry, True),
                                                 None))

    def is_connected(self, entry: str) -> bool:
        """Determines whether the specified entry name (**`system:capture_1`**)
        is connected to another entry.

        Args:
            entry (str): The entry name to match.

        Returns:
            bool: True, if the is connected; false, otherwise.
        """

        assert isinstance(entry, str) and entry.strip()

        if not self.is_entry(entry):
            return False

        # Check either key combination, or default.
        others = self._values.get((entry, False),
                                  self._values.get((entry, True),
                                                   None))
        return bool(others)

    def is_connected_to(self, entry: str, other: str) -> bool:
        """Determines whether the specified entry name (**`system:capture_1`**)
        is connected to other name (**`system:playback_1`**).

        Args:
            entry (str): The entry name to match.
            other (str): The other name to match.

        Returns:
            bool: True, if the is connected; false, otherwise.
        """

        assert isinstance(entry, str) and entry.strip()
        assert isinstance(other, str) and other.strip()

        if not self.is_entry(entry):
            return False

        # Check either key combination, or default.
        others = self._values.get((entry, False),
                                  self._values.get((entry, True),
                                                   None))
        return other in others

    def get_ports(self, client: str) -> list[str]:
        """Returns ports of specified client (**`system`**) name.

        Returns:
            list (str): A list of all ports for the specified client. If client
                does not exist, an empty list is returned.
        """

        assert isinstance(client, str) and client.strip()

        if not self.is_client(client):
            return []

        result = [ConnectionInfo.from_entry(e[self.IDX_NAME])[self.IDX_PORT]
                  for e in self._values.keys()
                  if ConnectionInfo.from_entry(
                      e[self.IDX_NAME])[self.IDX_CLIENT] == client]
        return result

    def get_entries(self, client: str) -> list[str]:
        """Returns entries of specified client (**`system`**) name.

        Returns:
            list (str): A list of all entries for the specified client. If
                client does not exist, an empty list is returned.
        """

        assert isinstance(client, str) and client.strip()

        if not self.is_client(client):
            return []

        result = [e[self.IDX_NAME]
                  for e in self._values.keys()
                  if ConnectionInfo.from_entry(
                      e[self.IDX_NAME])[self.IDX_CLIENT] == client]
        return result

    def _group_by_client(
            self,
    ) -> dict[str, list[tuple[str, str]]]:
        """Returns connecections grouped by client names.

        * `'system'`
            * `'system:capture_1' : 'system:playback_1'`
            * `'system:capture_2' : 'system:playback_2'`

        Args:
            port_only (bool): True, if the values only contain `port` 
                information for source (`capture_1`, `playback_2`); false, if
                the values the full entry (`system:capture_1`,
                `system:playback_2`) (*default*).

        Returns:
            dict (str, list[tuple[str, str]]): Keys contain client names; each
                value list tuple contains port/entry or entry/entry names.
        """

        result: dict[str, list[str]] = {}

        for entry_type, others in self._values.items():
            entry, is_sink = entry_type
            client, _ = ConnectionInfo.from_entry(entry)

            if client not in result:
                result[client] = []

            for other in others:

                if is_sink:
                    result[client].append((other, entry))
                else:
                    result[client].append((entry, other))
        return result

    def clone(self) -> dict[tuple[str, bool], list[str]]:
        """Deep clone and sort the connection info."""

        result: dict[tuple[str, bool], list[str]] = {}

        for entry, others in self._values.items():
            sorted_others = sorted(others)
            result[entry] = sorted_others

        return dict(sorted(result.items()))

    def __str__(self) -> str:
        return "\n".join(
            f"{key[0]} ({'source' if not key[1] else 'sink'}): "
            f"{', '.join(values)}"
            for key, values in self._values.items()
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConnectionInfo):
            raise NotImplementedError(f"other '{type(other)}'")
        return self._values == other._values

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
