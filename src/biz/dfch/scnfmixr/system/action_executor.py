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
