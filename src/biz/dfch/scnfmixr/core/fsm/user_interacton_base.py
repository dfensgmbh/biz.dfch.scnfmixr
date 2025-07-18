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
