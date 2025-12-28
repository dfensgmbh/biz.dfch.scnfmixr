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

"""Module jack_source_point."""

from __future__ import annotations
from typing import TYPE_CHECKING

from ..public.mixer import (
    ConnectionPolicy,
    IConnectableSink,
)
from .source_point import SourcePoint
if TYPE_CHECKING:
    from .jack_signal_manager import JackSignalManager


__all__ = [
    "JackSourcePoint",
]


class JackSourcePoint(
        SourcePoint,
):
    """Represents a JACK ALSA source point."""

    _mgr: "JackSignalManager"

    def __init__(self, name, info):
        super().__init__(name, info)

        from .jack_signal_manager import JackSignalManager\
            # pylint: disable=C0415

        self._mgr = JackSignalManager.Factory.get()

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):

        assert isinstance(other, IConnectableSink)
        if ConnectionPolicy.DEFAULT == policy:
            policy = ConnectionPolicy.MONO

        result = self._mgr.get_signal_paths(
            self, other, policy)

        assert isinstance(result, list) and 1 == len(result), result

        _, path = result[0]
        path.acquire()

        return result
