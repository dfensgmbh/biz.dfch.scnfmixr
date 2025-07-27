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

"""Module signal_point."""

from ..public.mixer import IConnectablePoint, ConnectionInfo, State
from .acquirable_point_mixin import AcquirablePointMixin


__all__ = [
    "SourceOrSinkPoint",
]


class SourceOrSinkPoint(IConnectablePoint, AcquirablePointMixin):
    """Represents a source or sink point."""

    _info: ConnectionInfo

    def __init__(self, name: str, info: ConnectionInfo):
        super().__init__(name)

        assert isinstance(name, str) and name.strip()
        assert isinstance(info, ConnectionInfo)

        self._info = info

    @property
    def is_active(self):
        return self.state.has_flag(State.Flag.OK)

    def do_acquire(self):
        self.state.set_flag(State.Flag.INITIAL)
        self.state.is_acquired = True

        return self

    def do_release(self):
        self.state.set_flag(State.Flag.REMOVED)
        self.state.is_acquired = False

    def _on_message(self, _):
        return

    @property
    def is_acquired(self) -> bool:
        return self.state.is_acquired

    @is_acquired.setter
    def is_acquired(self, value: bool) -> None:

        assert isinstance(value, bool)

        self.state.is_acquired = True
