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

"""Module path_state_flag."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntFlag
from threading import Lock


@dataclass
class State:
    """Represents the state of an ISignalPath."""

    class Flag(IntFlag):
        """The states of a path."""
        INITIAL = 0x01
        DEFAULT = INITIAL
        OK = 0x02
        STALE = 0x04
        REMOVED = 0x08
        ACQUIRED = 0x80

        RELEASED_INITIAL = INITIAL
        RELEASED_OK = OK
        RELEASED_STALE = STALE
        RELEASED_REMOVED = REMOVED
        ACQUIRED_INITIAL = ACQUIRED | INITIAL
        ACQUIRED_OK = ACQUIRED | OK
        ACQUIRED_STALE = ACQUIRED | STALE
        ACQUIRED_REMOVE = ACQUIRED | REMOVED
    _sync_root: Lock = field(default_factory=Lock, init=False, repr=False)

    _value: State.Flag = field(
        init=False, default=Flag.INITIAL)

    @property
    def name(self) -> str:
        """Return a string representation of the currently set flag."""
        return str(self)

    @property
    def is_acquired(self) -> bool:
        """Determines whether the ACQUIRED flag is set or not."""
        with self._sync_root:
            return bool(self._value & State.Flag.ACQUIRED)

    @is_acquired.setter
    def is_acquired(self, value: bool) -> None:
        """Sets or clears the ACQUIRED flag."""
        assert isinstance(value, bool)

        with self._sync_root:
            if value:
                self._value |= State.Flag.ACQUIRED
            else:
                self._value &= ~State.Flag.ACQUIRED

    @property
    def value(self) -> State.Flag:
        """Returns the path state."""
        with self._sync_root:
            return self._value

    @value.setter
    def value(self, new_value: State.Flag) -> None:
        """Sets the path state."""

        assert isinstance(new_value, State.Flag)

        with self._sync_root:
            acquired_set = self._value & State.Flag.ACQUIRED
            base_state = new_value & ~State.Flag.ACQUIRED
            self._value = base_state | acquired_set

    def has_flag(self, flag: State.Flag) -> bool:
        """Determines whether the specified flag is set or not."""
        assert isinstance(flag, State.Flag)
        return (self._value & flag) == flag

    def set_flag(self, new_flag: State.Flag) -> None:
        """Sets the base flag (INITIAL, OK, STALE, REMOVED) while preserving
        ACQUIRED."""

        assert isinstance(new_flag, State.Flag)
        assert new_flag in (
            State.Flag.INITIAL,
            State.Flag.OK,
            State.Flag.STALE,
            State.Flag.REMOVED,
        ), new_flag

        with self._sync_root:
            acquired = self._value & State.Flag.ACQUIRED
            self._value = new_flag | acquired

    def __str__(self) -> str:
        return self._value.name or f"{self._value:#x}"

    def __repr__(self) -> str:
        return self.__str__()
