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
    "Message",
    "MessageHigh",
    "MessageMedium",
    "MessageLow",
]


@dataclass(frozen=True)
class MessageBase(ABC):
    """A base class for messages.

    Attributes:
        name (str): The message type name.
        priority (MessagePriority): The message priority.
            Default: `MessagePriority.DEFAULT`.
    """

    name: str
    priority: MessagePriority

    def __init__(
            self,
            name: str,
            priority: MessagePriority = MessagePriority.DEFAULT
    ) -> None:
        """Default ctor.

        Args:
            name (str): The message type name.
            priority (MessagePriority): The message priority.
                Default: `MessagePriority.DEFAULT`.
        """

        assert name and name.strip()
        assert priority and isinstance(property, MessagePriority)

        self.priority = priority
        self.name = name


@dataclass(frozen=True)
class MessageHigh(MessageBase):
    """A message with priority `MessagePriority.HIGH`.

    Attributes:
        name (str): The message type name.
    """

    def __init__(
            self,
            name: str,
    ) -> None:
        """Default ctor.

        Args:
            name (str): The message type name.
        """

        super().__init__(name, MessagePriority.HIGH)


@dataclass(frozen=True)
class MessageMedium(MessageBase):
    """A message with priority `MessagePriority.MEDIUM`.

    Attributes:
        name (str): The message type name.
    """

    def __init__(
            self,
            name: str,
    ) -> None:
        """Default ctor.

        Args:
            name (str): The message type name.
        """

        super().__init__(name, MessagePriority.MEDIUM)


# Alias for MessageMedium
Message = MessageMedium


@dataclass(frozen=True)
class MessageLow(MessageBase):
    """A message with priority `MessagePriority.LOW`.

    Attributes:
        name (str): The message type name.
    """

    def __init__(
            self,
            name: str,
    ) -> None:
        """Default ctor.

        Args:
            name (str): The message type name.
        """

        super().__init__(name, MessagePriority.LOW)
