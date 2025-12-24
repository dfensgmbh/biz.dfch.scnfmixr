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

"""Module message_low."""

from .message_base import (
    MessageBase,
    ICommand,
    INotification,
)
from .message_priority import MessagePriority


__all__ = [
    "MessageLow",
    "CommandLow",
    "NotificationLow",
]


class MessageLow(MessageBase):  # pylint: disable=R0903
    """A message with priority `MessagePriority.LOW`.

    Attributes:
    """

    def __init__(self) -> None:
        super().__init__(MessagePriority.LOW)


class CommandLow(MessageLow, ICommand):  # pylint: disable=R0903
    """A command message with priority `MessagePriority.LOW`"""


class NotificationLow(MessageLow, INotification):  # pylint: disable=R0903
    """A notification message with priority `MessagePriority.LOW`"""
