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

"""Module signal_handler."""

import signal

from ..public.messages import SystemMessage
from .message_queue import MessageQueue

__all__ = [
    "SignalHandler",
]


class SignalHandler:
    """Handles SIGINT und SIGTERM events."""

    _mq: MessageQueue

    def __init__(self):

        self._mq = MessageQueue.Factory.get()

        signal.signal(signal.SIGINT, self._on_signal)

    def _on_signal(self, signum, frame):
        """Message handler for SIGINT and SIGTERM."""

        _ = signum
        _ = frame

        self._mq.publish(SystemMessage.Shutdown())
