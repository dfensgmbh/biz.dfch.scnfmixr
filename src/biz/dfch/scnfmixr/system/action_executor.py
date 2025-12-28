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

"""Module action_executor."""

from ..public.system.message_base import IMessage
from .func_executor import FuncExecutor


class ActionExecutor(FuncExecutor[None]):
    """Publishes a message, waits for a return message and executes a specified
    action."""

    def invoke(
            self,
            message: IMessage,
            max_wait_time: float = 5,
    ) -> None:

        assert 0 < max_wait_time
        assert isinstance(message, IMessage)

        self._result = None
        self._signal.clear()

        self._mq.publish(message)

        self._signal.wait(max_wait_time)

        self.get_result()

    def wait(
            self,
            max_wait_time: float = 5,
    ) -> None:
        """Waits for a message."""

        assert 0 < max_wait_time

        self._result = None
        self._signal.clear()

        self._signal.wait(max_wait_time)

        self.get_result()
