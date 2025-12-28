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

"""Module signal_path."""

from __future__ import annotations

from biz.dfch.scnfmixr.mixer.signal_path_manager import SignalPathManager
from ..public.mixer import (
    ISignalPath,
    IConnectableSinkPoint,
    IConnectableSourcePoint,
)


class SignalPath(ISignalPath):
    """Represents a signal path between two connectable points."""

    _mgr: SignalPathManager
    _conn: SignalPathManager.Connection

    def __init__(self, source, sink, mgr: SignalPathManager):
        super().__init__(source, sink)

        assert isinstance(source, IConnectableSourcePoint)
        assert isinstance(sink, IConnectableSinkPoint)
        assert isinstance(mgr, SignalPathManager)

        self._mgr = mgr
        self._conn = SignalPathManager.Connection(source, sink)

    @property
    def is_active(self):
        return self._mgr.is_active(self._conn)

    def remove(self):
        raise NotImplementedError
