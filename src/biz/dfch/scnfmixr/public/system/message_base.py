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
            priority: MessagePriority = MessagePriority.DEFAULT
    ) -> None:
        """Default ctor.

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
