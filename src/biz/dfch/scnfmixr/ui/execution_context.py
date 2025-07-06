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

"""Module defining the transition context of the finite state machine."""

from dataclasses import dataclass, field
from threading import Event

from ...asyn import ConcurrentQueueT


@dataclass(frozen=True)
class ExecutionContext:
    """Defines the execution context of the finite state machine.

    Attributes:
        source (str | None): The transition or state which lead to the curent
            invocation.
        error (str | None): Not None if an error led to the current invocation.
            Can contain the failed transition name or state name.
        previous (str | None): The previous state of the state machine (if there
            one) or None.
        event (str | None): The event that invoked the transition. Or None, if
            invoked on a State.
        events (ConcurrentQueueT[str]): A queue for event signalling from inside
            the state machine.
        stop_engine (Event): Settings this event stop the state
            machine after the current invocation has completed.
    """

    source: str | None
    error: str | None
    previous: str | None = None
    event: str | None = None
    events: ConcurrentQueueT[str] = None
    signal_stop: Event = field(default_factory=Event)
