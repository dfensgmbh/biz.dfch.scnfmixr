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

"""Module returning_false."""

from ..fsm import TransitionBase, UiEventInfo, StateBase
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class ReturningFalse(TransitionBase):
    """Noop: this transition does nothing and returns False."""

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.RETURNING_FALSE_LEAVE, False),
            target_state=target)

    def invoke(self, _):
        return False
