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

"""Module defining the state of a finite state machine."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Self

from ...public.ui.ui_event_info import UiEventInfo
from .execution_context import ExecutionContext
from .transition_base import TransitionBase

__all__ = ["StateBase"]


@dataclass(frozen=True)
class StateBase:
    """Class for defining a state in a finite state machine.
        Attributes:
            info_start (EventAudioInfo, optional): The base (language
                independent) name for the info sound to be played when starting
                to execute the transition.
            info_end (EventAudioInfo, optional): The base (language
                independent) name for the info sound to be played when the
                transition has finished executing.
            transitions (list[Transition]): The list of available transitions
                for this state.
    """

    info_enter: UiEventInfo | None
    info_leave: UiEventInfo | None
    transitions: list[TransitionBase] = field(default_factory=list)

    def __post_init__(self):

        assert self.info_enter is None or isinstance(
            self.info_enter, UiEventInfo)
        assert self.info_leave is None or isinstance(
            self.info_leave, UiEventInfo)
        assert self.transitions is not None

    def on_enter(self, ctx: ExecutionContext) -> None:
        """Invoked upon entering the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx

    def on_leave(self, ctx: ExecutionContext) -> None:
        """Invoked upon leaving the state.

        Args:
            ctx (ExecutionContext): The execution context of the state machine.
        """

        assert ctx

    def add_transition(self, transition: TransitionBase) -> Self:
        """Adds a transition to a state.

        Returns:
            State: The current instance.

        Raises:
            AssertionError:  If the parameter given is not a valid transition
                object.
            AssertionError:  If a transition with the same event has already
                been added.
        """

        assert transition is not None
        assert isinstance(transition, TransitionBase)
        assert transition not in self.transitions
        # assert not any(type(t).__name__ == type(
        #     transition).__name__ for t in self.transitions), \
        #     f"Duplicate transition: '{transition.__class__.__name__}'."
        assert not any(t.event == transition.event for t in self.transitions), \
            f"Duplicate event: '{transition.event}' in " \
            f"'{transition.__class__.__name__}'."

        self.transitions.append(transition)

        return self
