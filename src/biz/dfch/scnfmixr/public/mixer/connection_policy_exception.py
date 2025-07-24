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
