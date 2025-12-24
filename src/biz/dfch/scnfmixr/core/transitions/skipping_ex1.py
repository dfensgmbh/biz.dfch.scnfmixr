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

"""Module skipping_ex1."""

from ..fsm import StateBase, TransitionBase
from ..fsm import UiEventInfo
from ..transition_event import TransitionEvent


class SkippingEx1(TransitionBase):
    """Skips EX1 audio device initialisation."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):
        return True
