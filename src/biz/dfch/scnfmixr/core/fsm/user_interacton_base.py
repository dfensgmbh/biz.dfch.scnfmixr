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

"""Module user_interaction_base."""

from abc import ABC, abstractmethod

from ...system import MessageQueue
from ...public.system import MessageBase

from ...public.ui.ui_event_info import UiEventInfo


# pylint: disable=R0903
class UserInteractionBase(ABC):
    """Base class for user interaction."""

    _message_queue: MessageQueue

    def __init__(self):
        super().__init__()

        self._message_queue = MessageQueue.Factory.get()

    @abstractmethod
    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

    # @abstractmethod
    # def update(self, item: UiEventInfo) -> None:
    #     """Updates the presentation layer."""

    #     assert item
    #     assert isinstance(item, UiEventInfo)
