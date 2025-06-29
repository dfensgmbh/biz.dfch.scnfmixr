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

"""Module defining the state of a finite state machine."""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from .ExecutionContext import ExecutionContext
from .StateInfoStart import StateInfoStart
from .StateInfoEnd import StateInfoEnd
from .TransitionBase import TransitionBase

__all__ = ["StateBase"]


@dataclass(frozen=True)
class StateBase(ABC):
    """Class for defining a state in a finite state machine.
        Attributes:
            info_start (StateInfoStart, optional):  The base (language
                independent) name for the info sound to be played when starting
                to execute the transition.
            info_end (StateInfoEnd, optional):  The base (language
                independent) name for the info sound to be played when the
                transition has finished executing.
            transitions (list[Transition]):  The list of available transitions
                for this state.
    """

    info_start: StateInfoStart
    info_end: StateInfoEnd
    transitions: list[TransitionBase] = field(default_factory=list)

    def __post_init__(self):

        assert self.info_start is None or isinstance(
            self.info_start, StateInfoStart)
        assert self.info_end is None or isinstance(
            self.info_end, StateInfoEnd)
        assert self.transitions is not None

    def on_start(self, ctx: ExecutionContext) -> None:
        """Method to be invoked upon entering the state."""

    def on_end(self, ctx: ExecutionContext) -> None:
        """Method to be invoked upon exiting the state."""

    def add_transition(self, transition: TransitionBase) -> "StateBase":
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
        assert not any(type(t).__name__ == type(
            transition).__name__ for t in self.transitions)
        assert not any(t.event == transition.event for t in self.transitions)

        self.transitions.append(transition)
