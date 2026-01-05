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

"""Package system."""

from .system_time import SystemTime

from .message_base import (
    IMessage,
    MessageBase,
    ICommand,
    INotification
)
from .message_high import (
    MessageHigh,
    CommandHigh,
    NotificationHigh,
)
from .message_medium import (
    Message,
    MessageMedium,
    CommandMedium,
    NotificationMedium,
)
from .message_low import (
    MessageLow,
    CommandLow,
    NotificationLow,
)
from .message_priority import MessagePriority


__all__ = [
    "IMessage",
    "MessageBase",
    "ICommand",
    "INotification",
    "MessageHigh",
    "CommandHigh",
    "NotificationHigh",
    "Message",
    "MessageMedium",
    "CommandMedium",
    "NotificationMedium",
    "MessageLow",
    "CommandLow",
    "NotificationLow",
    "MessagePriority",
    "SystemTime",
]
