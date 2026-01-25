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

"""action_descriptor"""

from dataclasses import dataclass
from typing import Callable

from biz.dfch.scnfmixr.public.system import MessageBase


@dataclass(frozen=True)
class ActionDescriptor:
    """A item in the callback list.

    Attributes:
        action: The callback to invoke.
        predicate: The filter to determine, if the callback shall be invoked.
    """

    action: Callable[[MessageBase], None]
    predicate: Callable[[MessageBase], bool] | None = None

    def get_key(self, action) -> str:
        """Gets the full qualified name of the action."""

        code = getattr(action, '__code__', None)
        if code:
            result = (
                f"{action.__module__}."
                f"{action.__qualname__}@{code.co_filename}:"
                f"{code.co_firstlineno}"
            )
        else:
            result = (
                f"{action.__module__}."
                f"{action.__qualname__}@{id(action)}"
            )
        return result
