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

"""Module defining a finite state machine."""

from __future__ import annotations
from enum import Enum
import threading
from log import log
from .ExecutionContext import ExecutionContext
from .StateBase import StateBase

__all__ = ["Fsm"]


def _(value: object) -> str:
    """Custom translator."""

    if isinstance(value, Enum):
        return value.name

    return value


class Fsm:
    """Class for defining a finite state machine.

    Attributes:
        current_state (State): The current state of the state machine.
    """

    def __init__(self, initial_state: StateBase, ctx: ExecutionContext) -> None:
        """Initialise a finite state machine.

        Attributes:
            initial_state (State): The initial state of the state machine.
        Returns:
            An instance of this class.
        Raises:
            AssertionError: When `initial_state` is `None`.
        """

        assert initial_state is not None
        assert isinstance(initial_state, StateBase)
        assert ctx is not None
        assert isinstance(ctx, ExecutionContext)

        self._initial_state = initial_state
        self._current_state = self._initial_state
        self._is_in_transit = False

        self._execution_context = ctx

        self._sync_root = threading.Lock()

    @property
    def current_state(self) -> StateBase:
        """Returns the current state of the finite state machine.

        Returns:
            State: The current state of the finite state machine.
        """

        with self._sync_root:
            return self._current_state

    @property
    def is_in_transit(self) -> bool:
        """Tests, if the finite state machine is currently transiting to
        another state.

        Returns:
            bool: True, if finite state machine is currently transiting to
            another state; False otherwise.
        """

        return self._is_in_transit

    def _to_string_internal(
            self,
            state: StateBase,
            indent: int,
            processed_states: set[int]
    ) -> list[str]:
        """
        Returns:
            list[str]:  The array containing the states and transitions.
        """

        DELIMITER: str = "#"  # pylint: disable=C0103
        SPACE: str = " "  # pylint: disable=C0103

        result: list[str] = []

        indent += 2

        prefix = indent * DELIMITER
        state_name = type(state).__name__
        state_hash = hash(type(state))

        if state_hash in processed_states:
            return result

        line = "%s '%s' [%s]" % (  # pylint: disable=C0209
            prefix,
            state_name,
            state_hash)
        result.append(line)

        processed_states.add(state_hash)

        for transition in state.transitions:

            prefix = indent * SPACE
            transition_name = type(transition).__name__
            transition_hash = hash(type(transition))
            target_state_name = type(transition.target_state).__name__
            target_state_hash = hash(type(transition.target_state))

            line = "%s '%s' [%s] -- > '%s' [%s] -- > '%s' [%s]" % (  # pylint: disable=C0209
                prefix,
                state_name,
                state_hash,
                transition_name,
                transition_hash,
                target_state_name,
                target_state_hash)
            result.append(line)

            items = self._to_string_internal(
                transition.target_state,
                indent,
                processed_states
            )
            result.extend(items)

        indent -= 2

        return result

    def visualise(self) -> list[str]:
        """Visualises the finite state machine.

        Attributes:
            None.

        Returns:
            list[str]: a array representing the states and transitions of the
            finite state machine.
        """

        processed_states: set[int] = set()
        result: list[str] = []
        indent = 0

        items = self._to_string_internal(
            self._initial_state,
            indent,
            processed_states
        )
        result.extend(items)

        return result

    def invoke(self, event: str) -> bool:
        """Invokes a transition for the current state based on the specified
        event.

        Attributes:
            event (str): The event to process.
        Returns:
            bool: True, if the specified `event` was valid in the current;
            False otherwise.
        Raises:
            AssertionError: Raised if event contains multiple characters.
        """

        assert event and event.strip()

        result = False

        with self._sync_root:

            log.debug("Finding transition in current state '%s' for "
                      "event '%s' [%s] ...",
                      _(self._current_state),
                      event,
                      len(self._current_state.transitions)
                      )

            transition = next((t for t in self._current_state.transitions
                               if t.event == event), None)
            if not transition:
                log.warning("Finding transition in current state '%s' for "
                            "event '%s' [%s] FAILED.",
                            _(self._current_state),
                            event,
                            len(self._current_state.transitions)
                            )
                return False

            log.info("Found transition in current state '%s' for event '%s' "
                     " [%s]: '%s' [target: %s].",
                     _(self._current_state),
                     event,
                     len(self._current_state.transitions),
                     _(type(transition).__name__),
                     _(transition.target_state)
                     )

            self._is_in_transit = True

            if self._current_state.info_end:
                # DFTODO: async play audio.
                pass

            log.debug("Invoking 'on_end' for '%s' ...",
                      type(self._current_state).__name__)
            self._current_state.on_end(self._execution_context)
            log.info("Invoking 'on_end' for '%s' RETURNED.",
                     type(self._current_state).__name__)

            if transition.info_start:
                # DFTODO: async play audio.
                pass

            log.debug("Invoking transition '%s' for '%s' ...",
                      type(transition).__name__,
                      type(self._current_state).__name__)
            result = transition.invoke(self._execution_context)

            self._is_in_transit = False

            if not result:
                log.error("Invoking transition '%s' for '%s' FAILED.",
                          type(transition).__name__,
                          type(self._current_state).__name__)

                log.debug("Invoking 'on_start' for '%s' ...",
                          type(self._current_state).__name__)
                self._current_state.on_start(self._execution_context)
                log.info("Invoking 'on_start' for '%s' RETURNED.",
                         type(self._current_state).__name__)

            log.info("Invoking transition '%s' for '%s' SUCCEEDED.",
                     type(transition).__name__,
                     type(self._current_state).__name__)

            if transition.info_end:
                # DFTODO: async play audio.
                pass

            self._current_state = transition.target_state

            if self._current_state.info_start:
                # DFTODO: async play audio.
                pass

            log.debug("Invoking 'on_start' for '%s' ...",
                      type(self._current_state).__name__)
            self._current_state.on_start(self._execution_context)
            log.info("Invoking 'on_start' for '%s' RETURNED.",
                     type(self._current_state).__name__)

        return result
