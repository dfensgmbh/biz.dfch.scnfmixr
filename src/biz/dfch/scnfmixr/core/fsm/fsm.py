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

from biz.dfch.logging import log

from .execution_context import ExecutionContext
from .state_base import StateBase
from ...public.system.messages import SystemMessage
from ...system import MessageQueue

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

    _message_queue = MessageQueue
    _initial_state: StateBase
    _current_state: StateBase
    _previous_state: StateBase
    _is_in_transit: bool
    _initial_context: ExecutionContext
    _sync_root: threading.RLock
    _sync_restart: threading.Lock

    def __init__(
        self,
        initial_state: StateBase,
        ctx: ExecutionContext,
    ) -> None:
        """Initialise a finite state machine.

        Args:
            initial_state (State): The initial state of the state machine.
            ctx (ExecutionContext): The initial execution context.

        Returns:
            An instance of this class.

        Raises:
            AssertionError: If `initial_state` is `None`.
            AssertionError: If `ctx` is `None`.
        """

        assert initial_state is not None
        assert isinstance(initial_state, StateBase)
        assert ctx is not None
        assert isinstance(ctx, ExecutionContext)

        self._message_queue = MessageQueue.Factory.get()
        self._is_started = False
        self._initial_state = initial_state
        self._current_state = self._initial_state
        self._previous_state = None
        self._is_in_transit: bool = False

        self._initial_context = ctx

        self._sync_root = threading.RLock()
        self._sync_restart = threading.Lock()

    @property
    def is_started(self) -> bool:
        """Determines whether the state machine is currently started.

        Returns:
            bool: True, if the state machine is started; false otherwise.
        """

        return self._is_started

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

    # pylint: disable=R0914
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

            prefix = indent * DELIMITER
            transition_name = type(transition).__name__
            transition_hash = hash(type(transition))
            target_state_name = type(transition.target_state).__name__
            target_state_hash = hash(type(transition.target_state))

            line = "%s '%s' [%s] -- > '%s' [%s] -- > '%s' [%s]" % (  # pylint: disable=C0209 # noqa E501
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

        return sorted(result)

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

    def start(self) -> bool:
        """Starts the state machine.

        Returns:
            bool: True, if the state machine could be started; false is the
                state machine was already started.

        Raises:
            Exception: Raises an exception if the state machine could not be
                started.
        """

        log.info("Starting state machine ...")
        self._message_queue.publish(
            SystemMessage.StateMachine.StateMachineStarting())

        if self._is_started:
            log.warning("Starting state machine FAILED. Already started. [1]")
            return False

        with self._sync_root:
            if self._is_started:
                log.warning(
                    "Starting state machine FAILED. Already started. [2]")
                return False

            self._is_started = True
            self._current_state = self._initial_state
            self._previous_state = None

            log.debug("Invoking 'on_enter' for '%s' ...",
                      type(self._current_state).__name__)
            ctx = ExecutionContext(
                source=None,
                error=None,
                previous=self._previous_state,
                events=self._initial_context.events)
            self._current_state.on_enter(ctx)
            log.info("Invoking 'on_enter' for '%s' RETURNED.",
                     type(self._current_state).__name__)

        self._message_queue.publish(
            SystemMessage.StateMachine.StateMachineStarted())

        log.info("Starting state machine OK.")

        if ctx.signal_stop.is_set():
            ctx.signal_stop.clear()
            log.info("Stop signal detected.")

            self.stop()

            return False

        return True

    def stop(self) -> None:
        """Stops the state machine.

        Returns:
            bool: True, if the state machine could be stopped; false if the
                state machine was already stopped.

        Raises:
            Exception: Raises an exception if the state machine could not be
                stopped.
        """

        log.info("Stopping state machine ...")
        self._message_queue.publish(
            SystemMessage.StateMachine.StateMachineStopping())

        if not self._is_started:
            log.warning(
                "Stopping state machine FAILED: Already stopped [1].")
            return False

        with self._sync_root:
            if not self._is_started:
                log.warning(
                    "Stopping state machine FAILED: Already stopped [2].")
                return False

            self._is_started = False

        self._message_queue.publish(
            SystemMessage.StateMachine.StateMachineStopped())
        log.info("Stopping state machine OK.")

        return True

    def restart(self) -> None:
        """Stops and starts the state machine. Only starts the state machine if
        the state machine was not already started.

        Returns:
            bool: True, if the state machine was previously started and was
                restarted; false if the state machine was previously not
                started but could be started.

        Raises:
            Exception: Raises an exception if the state machine could not be
                stopped or started.
        """

        log.info("Restarting state machine ...")

        with self._sync_restart:
            result = self._is_started
            if result:
                self.stop()

            self.start()

        log.info("Restarting state machine OK.")

        return result

    # pylint: disable=R0911
    def invoke(self, event: str) -> bool:
        """Invokes a transition for the current state based on the specified
        event.

        Attributes:
            event (str): The event to process.
        Returns:
            bool: True, if the specified `event` was valid in the current and
            was successfully invoked; false otherwise.
        Raises:
            AssertionError: Raised if event contains multiple characters.
        """

        assert event and event.strip()

        if not self._is_started:
            return False

        with self._sync_root:

            log.debug("Finding transition in current state '%s' for "
                      "event '%s' [%s] ...",
                      _(self._current_state.__class__.__name__),
                      event,
                      len(self._current_state.transitions)
                      )

            transition = next((t for t in self._current_state.transitions
                               if t.event == event), None)
            if not transition:
                log.warning("Finding transition in current state '%s' for "
                            "event '%s' [%s] FAILED.",
                            _(self._current_state.__class__.__name__),
                            event,
                            len(self._current_state.transitions)
                            )

                return False

            log.info("Found transition in current state '%s' for event '%s' "
                     " [%s]: '%s' [target: %s].",
                     _(self._current_state.__class__.__name__),
                     event,
                     len(self._current_state.transitions),
                     _(type(transition).__name__),
                     _(transition.target_state.__class__.__name__)
                     )

            self._is_in_transit = True

            if self._current_state.info_leave:
                # self._ui.update(self.current_state.info_leave)
                self._message_queue.publish(
                    SystemMessage.UiEventInfoStateLeaveMessage(
                        self.current_state.info_leave))

            log.debug("Invoking 'on_leave' for '%s' ...",
                      type(self._current_state).__name__)
            ctx = ExecutionContext(
                source=type(self._current_state).__name__,
                error=None,
                previous=self._previous_state,
                events=self._initial_context.events)
            self._current_state.on_leave(ctx)
            log.info("Invoking 'on_leave' for '%s' RETURNED.",
                     type(self._current_state).__name__)

            if ctx.signal_stop.is_set():
                ctx.signal_stop.clear()
                log.info("Stop signal detected.")

                self.stop()

                return False

            if transition.info_enter:
                # self._ui.update(transition.info_enter)
                self._message_queue.publish(
                    SystemMessage.UiEventInfoTransitionEnterMessage(
                        transition.info_enter))

            log.debug("Invoking transition '%s' for '%s' ...",
                      type(transition).__name__,
                      type(self._current_state).__name__)
            ctx = ExecutionContext(
                source=type(self._current_state).__name__,
                error=None,
                previous=self._previous_state,
                event=event,
                events=self._initial_context.events)
            result = transition.invoke(ctx)

            self._is_in_transit = False

            if not result:
                log.error("Invoking transition '%s' for '%s' FAILED.",
                          type(transition).__name__,
                          type(self._current_state).__name__)

                log.debug("Invoking 'on_enter' for '%s' ...",
                          type(self._current_state).__name__)

                # self._ui.update(self.current_state.info_enter)
                self._message_queue.publish(
                    SystemMessage.UiEventInfoStateEnterMessage(
                        self.current_state.info_enter))

                ctx = ExecutionContext(
                    source=type(self._current_state).__name__,
                    error=type(transition).__name__,
                    previous=self._previous_state,
                    events=self._initial_context.events)
                self._current_state.on_enter(ctx)
                log.info("Invoking 'on_enter' for '%s' RETURNED.",
                         type(self._current_state).__name__)

                if ctx.signal_stop.is_set():
                    ctx.signal_stop.clear()
                    log.info("Stop signal detected.")

                    self.stop()

                    return False

                return result

            log.info("Invoking transition '%s' for '%s' OK.",
                     type(transition).__name__,
                     type(self._current_state).__name__)

            if transition.info_leave:
                # self._ui.update(transition.info_leave)
                self._message_queue.publish(
                    SystemMessage.UiEventInfoTransitionLeaveMessage(
                        transition.info_leave))

            self._previous_state = self._current_state
            self._current_state = transition.target_state
            log.info("State changed. Previous: '%s'. Current: '%s'.",
                     self._previous_state.__class__.__name__,
                     self._current_state.__class__.__name__)

            if ctx.signal_stop.is_set():
                ctx.signal_stop.clear()
                log.info("Stop signal detected.")

                self.stop()
                # Do not return False here, as the transition itself succeeded.
                return True

            if self._current_state.info_enter:
                # self._ui.update(self._current_state.info_enter)
                self._message_queue.publish(
                    SystemMessage.UiEventInfoStateEnterMessage(
                        self.current_state.info_enter))

            log.debug("Invoking 'on_enter' for '%s' ...",
                      type(self._current_state).__name__)
            ctx = ExecutionContext(
                source=type(transition).__name__,
                error=None,
                previous=self._previous_state,
                events=self._initial_context.events)
            self._current_state.on_enter(ctx)
            log.info("Invoking 'on_enter' for '%s' RETURNED.",
                     type(self._current_state).__name__)

            if ctx.signal_stop.is_set():
                ctx.signal_stop.clear()
                log.info("Stop signal detected.")

                self.stop()
                # Do not return False here, as the transition itself succeeded.

        return True
