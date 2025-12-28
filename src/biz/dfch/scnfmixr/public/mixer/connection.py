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

"""Module connection_parameters."""

from dataclasses import dataclass

from .constant import Constant


@dataclass(frozen=True)
class Connection:
    """Parameters for a routing entry."""

    this: str
    other: str
    idx_this: int = 0
    idx_other: int = 0

    @staticmethod
    def source(value: str) -> str:
        """Gets the source name of the specified value.

        `value` -- > `value`**`-I`**.
        """

        assert value and value.strip()

        input_suffix = f"{Constant.JACK_INFIX}{Constant.JACK_INPUT}"

        if value.endswith(input_suffix):
            return value

        return f"{value}{input_suffix}"

    @staticmethod
    def sink(value: str) -> str:
        """Gets the sink name of the specified value.

        `value` -- > `value`**`-O`**.
        """

        assert value and value.strip()

        output_suffix = f"{Constant.JACK_INFIX}{Constant.JACK_OUTPUT}"

        if value.endswith(output_suffix):
            return value

        return f"{value}{output_suffix}"

    @staticmethod
    def jack_alsa_client_from_base(value: str) -> str:
        """Returns **`Alsa:<value>`**."""
        return Connection.jack_client_from_base(
            Constant.JACK_ALSA_PREFIX, value)

    @staticmethod
    def jack_mixbus_client_from_base(value: str) -> str:
        """Returns **`Mixbus:<value>`**."""
        return Connection.jack_client_from_base(
            Constant.JACK_MIXBUS_PREFIX, value)

    @staticmethod
    def jack_client_from_base(prefix: str, value: str) -> str:
        """Returns **`<prefix>:<value>`**."""

        result = (
            f"{prefix}"
            f"{Constant.JACK_SEPARATOR}"
            f"{value}"
        )
        return result

    @staticmethod
    def jack_alsa_client_source_prefix(value: str) -> str:
        """Returns **`Alsa:<value>-I`**."""

        result = (
            f"{Connection.jack_alsa_client_from_base(value)}"
            f"{Constant.JACK_INFIX}"
            f"{Constant.JACK_INPUT}"
        )
        return result

    @staticmethod
    def jack_mixbus_client_source_prefix(value: str) -> str:
        """Returns **`Mixbus:<value>-I`**."""

        result = (
            f"{Connection.jack_mixbus_client_from_base(value)}"
            f"{Constant.JACK_INFIX}"
            f"{Constant.JACK_INPUT}"
        )
        return result

    @staticmethod
    def jack_alsa_client_sink_prefix(value: str) -> str:
        """Returns **`Alsa:<value>-O`**."""

        result = (
            f"{Connection.jack_alsa_client_from_base(value)}"
            f"{Constant.JACK_INFIX}"
            f"{Constant.JACK_OUTPUT}"
        )
        return result

    @staticmethod
    def jack_mixbus_client_sink_prefix(value: str) -> str:
        """Returns **`Mixbus:<value>-O`**."""

        result = (
            f"{Connection.jack_mixbus_client_from_base(value)}"
            f"{Constant.JACK_INFIX}"
            f"{Constant.JACK_OUTPUT}"
        )
        return result

    @staticmethod
    def get_jack_source_port_names(count: int, client: str = "") -> list[str]:
        """Returns a list of JACK source port or entry names.

        Index starts at `1`, eg. `capture_1`.

        Args:
            count (int): The number of port or entry names to return.
            client (str): The client name to create the entry from. If empty,
                only the port name with be created.

        Retunrs:
            list (str): The list with port or entry names.
        """

        assert isinstance(count, int) and 0 < count

        result: list[str] = []

        for i in range(count):
            idx = i + 1

            if client is not None and client.strip():
                result.append(
                    f"{client}"
                    f"{Constant.JACK_SEPARATOR}"
                    f"{Constant.JACK_SOURCE_PORT_INFIX_BASE}"
                    f"{idx}")
            else:
                result.append(
                    f"{Constant.JACK_SOURCE_PORT_INFIX_BASE}"
                    f"{idx}")

        return result

    @staticmethod
    def get_jack_sink_port_names(count: int, client: str = "") -> list[str]:
        """Returns a list of JACK sink port or entry names.

        Index starts at `1`, eg. `playback_1`.

        Args:
            count (int): The number of port or entry names to return.
            client (str): The client name to create the entry from. If empty,
                only the port name with be created.

        Retunrs:
            list (str): The list with port or entry names.
        """

        result: list[str] = []

        for i in range(count):
            idx = i + 1

            if client is not None and client.strip():
                result.append(
                    f"{client}"
                    f"{Constant.JACK_SEPARATOR}"
                    f"{Constant.JACK_SINK_PORT_INFIX_BASE}"
                    f"{idx}")
            else:
                result.append(
                    f"{Constant.JACK_SINK_PORT_INFIX_BASE}"
                    f"{idx}")

        return result

    @staticmethod
    def get_jack_source_port_prefix() -> str:
        """Returns the source port prefix.

        **`capture`**
        """
        return Constant.JACK_SOURCE_PORT_INFIX_BASE.strip('_')

    @staticmethod
    def get_jack_sink_port_prefix() -> str:
        """Returns the sink port prefix.

        **`playback`**
        """
        return Constant.JACK_SINK_PORT_INFIX_BASE.strip('_')
