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

"""Module defining the transition of a state in a finite state machine."""

from __future__ import annotations
from dataclasses import dataclass
# Note: Python is a mess. We cannot have circular dependencies and thus cannot
# import `State` directly but have to use TYPE_CHECKING and __future__ with
# type quoting it.
from typing import TYPE_CHECKING

from ...public.ui.ui_event_info import UiEventInfo
from .execution_context import ExecutionContext

if TYPE_CHECKING:
    from .state_base import StateBase


@dataclass(frozen=True)
class TransitionBase:
    """Class for the definition of a transition in a state in a finite state
        machine.
        Attributes:
            event (str):  The event that triggers this transition.
            target_state (State):  The state to which this transition leads to.
            info_enter (EventAudioInfo, optional):  The base (language
                independent) name for the info sound to be played when starting
                to execute the transition.
            info_leave (EventAudioInfo, optional):  The base (language
                independent) name for the info sound to be played when the
                transition has finished executing.
    """

    event: str
    # See remark at top regarding circular dependencies and quoting types.
    target_state: "StateBase"
    info_enter: UiEventInfo | None = None
    info_leave: UiEventInfo | None = None

    def __post_init__(self) -> None:
        """Field validation."""

        # See remark at top regarding circular dependencies and importing.
        from .state_base import StateBase  # pylint: disable=C0415

        assert self.event and 1 == len(self.event)
        assert self.info_enter is None or isinstance(
            self.info_enter, UiEventInfo)
        assert self.info_leave is None or isinstance(
            self.info_leave, UiEventInfo)
        assert self.target_state is not None
        assert isinstance(self.target_state, StateBase)

    def invoke(self, ctx: ExecutionContext) -> bool:
        """Invokes the actual transition.

        Always returns true.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.

        Returns:
            bool: True, if the transition was successful; false otherwise.
        """

        assert ctx is not None
        assert isinstance(ctx, ExecutionContext)

        return True
