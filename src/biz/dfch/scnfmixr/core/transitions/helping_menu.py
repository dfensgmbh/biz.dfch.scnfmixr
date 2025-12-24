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

"""Module helping_menu."""

from ..fsm import StateBase, TransitionBase, UiEventInfo
from ..transition_event import TransitionEvent


__all__ = [
    "HelpingPlayback",
    "HelpingOnRecord",
]


class HelpingPlayback(TransitionBase):
    """Plays the help message of the Playback menu."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.HELPING_PLAYBACK_LEAVE, False),
            target_state=target)


class HelpingOnRecord(TransitionBase):
    """Plays the help message of the OnRecord menu."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.HELPING_ONRECORD_LEAVE, False),
            target_state=target)
