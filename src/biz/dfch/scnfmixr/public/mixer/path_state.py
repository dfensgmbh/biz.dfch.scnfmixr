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

"""Module path_state_flag."""

from dataclasses import dataclass, field
from threading import Lock

from .path_state_flag import PathStateFlag


@dataclass
class PathState:
    """Represents the state of an ISignalPath."""

    _sync_root: Lock = field(default_factory=Lock, init=False, repr=False)

    _value: PathStateFlag = field(init=False, default=PathStateFlag.INITIAL)

    @property
    def is_acquired(self) -> bool:
        """Determines whether the ACQUIRED flag is set or not."""
        with self._sync_root:
            return bool(self._value & PathStateFlag.ACQUIRED)

    @is_acquired.setter
    def is_acquired(self, value: bool) -> None:
        """Sets or clears the ACQUIRED flag."""
        assert isinstance(value, bool)

        with self._sync_root:
            if value:
                self._value |= PathStateFlag.ACQUIRED
            else:
                self._value &= ~PathStateFlag.ACQUIRED

    @property
    def value(self) -> PathStateFlag:
        """Returns the path state."""
        with self._sync_root:
            return self._value

    @value.setter
    def value(self, new_value: PathStateFlag) -> None:
        """Sets the path state."""

        assert isinstance(new_value, PathStateFlag)

        with self._sync_root:
            acquired_set = self._value & PathStateFlag.ACQUIRED
            base_state = new_value & ~PathStateFlag.ACQUIRED
            self._value = base_state | acquired_set

    def has_flag(self, flag: PathStateFlag) -> bool:
        """Determines whether the specified flag is set or not."""
        assert isinstance(flag, PathStateFlag)
        return (self._value & flag) == flag

    def __str__(self) -> str:
        return self._value.name or f"{self._value:#x}"

    def __repr__(self) -> str:
        return self.__str__()
