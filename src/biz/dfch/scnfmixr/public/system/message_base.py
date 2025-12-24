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

"""Module message_base."""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from .message_priority import MessagePriority


__all__ = [
    "MessageBase",
    "ICommand",
    "INotification",
]


class IMessage:
    """Base interface for all messages."""


class ICommand(IMessage):
    """Base interface for all commands."""


class INotification(IMessage):
    """Base interface for all notifications."""


@dataclass(frozen=True)
class MessageBase(ABC, IMessage):
    """A base class for messages.

    Attributes:
        name (str): The full qualified type name.
        priority (MessagePriority): The message priority.
            Default: `MessagePriority.DEFAULT`.
    """

    id: str
    name: str
    priority: MessagePriority
    children: list[MessageBase]

    def __init__(
            self,
            priority: MessagePriority = MessagePriority.DEFAULT,
    ) -> None:
        """Creates an instance of the object.

        Args:
            priority (MessagePriority): The message priority.
                Default: `MessagePriority.DEFAULT`.
        """

        assert priority and isinstance(priority, MessagePriority)
        object.__setattr__(self, "priority", priority)

        _type = type(self)
        object.__setattr__(self, "name", MessageBase.get_fqcn(_type))

        object.__setattr__(self, "id", str(id(self)))

        object.__setattr__(self, "children", [])

    @staticmethod
    def get_fqcn(_type: type) -> str:
        """Returns the full qualified class name."""

        assert _type

        return f"{_type.__module__}.{_type.__qualname__}"
