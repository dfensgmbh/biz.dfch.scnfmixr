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

"""Module detecting_hi2."""

from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class DetectingHi2(TransitionBase):
    """Detecting device HI2."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI2_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.DETECTING_DEVICE_HI2_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):
        return True
