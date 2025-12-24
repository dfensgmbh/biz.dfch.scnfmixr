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

"""Module connection_policy_exception."""

from .connection_policy import ConnectionPolicy
from .iconnectable_source import IConnectableSource
from .iconnectable_sink import IConnectableSink


class ConnectionPolicyException(Exception):
    """Exception for ConnectionPolicy errors."""

    policy: str
    source: IConnectableSource
    sink: IConnectableSink
    message: str

    def __init__(
            self,
            policy: ConnectionPolicy,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> None:

        assert isinstance(policy, ConnectionPolicy)
        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        self.policy = policy
        self.source = source
        self.sink = sink

        if source.is_point and sink.is_point:
            self.message = (f"{policy.name}: An exception occurred "
                            f"while creating connections "
                            f"from source point '{source.name}' "
                            f"to sink point '{sink.name}'.")
        if source.is_point and sink.is_set:
            self.message = (f"{policy.name}: An exception occurred "
                            f"while creating connections "
                            f"from source point '{source.name}' "
                            f"to sink set '{sink.name}' [{len(sink.points)}].")
        if source.is_set and sink.is_point:
            self.message = (f"{policy.name}: An exception occurred "
                            f"while creating connections "
                            f"from source set '{source.name}' "
                            f"[{len(source.points)}] "
                            f"to sink point '{sink.name}'.")
        if source.is_set and sink.is_set:
            self.message = (f"{policy.name}: An exception occurred "
                            f"while creating connections "
                            f"from source set '{source.name}' "
                            f"[{len(source.points)}] "
                            f"to sink set '{sink.name}' [{len(sink.points)}].")

        self.message = f"{policy.name}: An exception occurred."

    def __str__(self) -> str:
        return self.message

    def __repr__(self):
        return self.__str__()
