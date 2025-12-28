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

"""Module deleting_last_take."""

from ..fsm import TransitionBase, UiEventInfo, StateBase
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class DeletingLastTake(TransitionBase):
    """This transition deletes the last take (in any).

    NOTE: At this time, the transition does nothing.
    """

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DELETING_LAST_TAKE_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DELETING_LAST_TAKE_LEAVE, False),
            target_state=target)

    def invoke(self, _):
        return True
