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

"""Module signal_point."""

from __future__ import annotations

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

    @property
    def is_source(self):

        from ..public.mixer import IConnectableSource \
            # pylint: disable=C0415

        return isinstance(self, IConnectableSource)

    @property
    def is_sink(self):

        from ..public.mixer import IConnectableSink \
            # pylint: disable=C0415

        return isinstance(self, IConnectableSink)
