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

"""Module defining the transition context of the finite state machine."""

from dataclasses import dataclass, field
from threading import Event

from ...system import MessageQueue


@dataclass(frozen=True)
class ExecutionContext:
    """Defines the execution context of the finite state machine.

    Attributes:
        source (str | None): The transition or state which lead to the current
            invocation.
        error (str | None): Not None if an error led to the current invocation.
            Can contain the failed transition name or state name.
        previous (str | None): The previous state of the state machine (if there
            is one) or None.
        event (str | None): The event that invoked the transition. Or None, if
            invoked on a State.
        events (MessageQueue): A queue for event signalling from inside
            the state machine.
        stop_engine (Event): Settings this event stop the state
            machine after the current invocation has completed.
    """

    source: str | None
    error: str | None
    previous: str | None = None
    event: str | None = None
    events: MessageQueue = None
    signal_stop: Event = field(default_factory=Event)
