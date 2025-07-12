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

"""Module defining the transition of a state in a finite state machine."""

from __future__ import annotations
from dataclasses import dataclass
# Note: Python is a mess. We cannot have circular dependencies and thus cannot
# import `State` directly but have to use TYPE_CHECKING and __future__ with
# type quoting it.
from typing import TYPE_CHECKING

from .ui_event_info import UiEventInfo
from .execution_context import ExecutionContext

if TYPE_CHECKING:
    from .state_base import StateBase


@dataclass(frozen=True)
class TransitionBase:
    """Class for the defintion of a transition in a state in a finite state
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
