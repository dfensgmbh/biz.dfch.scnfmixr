# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

import unittest
from threading import Thread
import time

from biz.dfch.logging import log

from biz.dfch.scnfmixr.system.message_queue import MessageQueue
from biz.dfch.scnfmixr.system.func_executor import FuncExecutor
from biz.dfch.scnfmixr.system.action_executor import ActionExecutor
from biz.dfch.scnfmixr.public.system import (
    MessageBase,
    NotificationMedium,
    CommandMedium
)


class TestFuncExecutor(unittest.TestCase):
    """Test"""

    class ANotification(NotificationMedium):
        """ANotification"""

        value: int

        def __init__(self, value: int):
            super().__init__()

            self.value = value

    class ACommand(CommandMedium):
        """ACommand"""

    def funcenstein(self, message: MessageBase) -> int:
        """Func that returns message.value."""

        assert isinstance(message, TestFuncExecutor.ANotification)

        log.debug("funcenstein '%s'", message.value)

        return message.value

    def action_throws(self, message: MessageBase) -> None:
        """Action that throws."""

        assert isinstance(message, TestFuncExecutor.ANotification)

        log.debug("action '%s'", message.value)

        raise ValueError(message.value)

    def _publish_message(self, expected: int) -> None:
        time.sleep(0.25)
        mq = MessageQueue.Factory.get()
        mq.publish(TestFuncExecutor.ANotification(expected))

    def test_invoke_func_succeeds(self):
        """test"""

        expected = 42

        thread = Thread(
            target=self._publish_message, args=[expected], daemon=True)
        thread.start()

        with FuncExecutor(
            self.funcenstein, lambda e: isinstance(
                e, TestFuncExecutor.ANotification)) as sync:
            result = sync.invoke(TestFuncExecutor.ACommand())

        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    def test_wait_func_succeeds(self):
        """test"""

        expected = 42

        thread = Thread(
            target=self._publish_message, args=[expected], daemon=True)
        thread.start()

        with FuncExecutor(
            self.funcenstein, lambda e: isinstance(
                e, TestFuncExecutor.ANotification)) as sync:
            result = sync.wait()

        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    def test_invoke_action_throws(self):
        """test"""

        expected = 42

        thread = Thread(
            target=self._publish_message, args=[expected], daemon=True)
        thread.start()

        with self.assertRaises(ValueError) as exc:
            with ActionExecutor(
                self.action_throws, lambda e: isinstance(
                    e, TestFuncExecutor.ANotification)) as sync:
                sync.invoke(TestFuncExecutor.ACommand())
            self.assertEqual(expected, exc.msg)

            log.debug(exc.msg)

    def test_wait_action_throws(self):
        """test"""

        expected = 42

        thread = Thread(
            target=self._publish_message, args=[expected], daemon=True)
        thread.start()

        with self.assertRaises(ValueError) as exc:
            with ActionExecutor(
                self.action_throws, lambda e: isinstance(
                    e, TestFuncExecutor.ANotification)) as sync:
                sync.wait()
            self.assertEqual(expected, exc.msg)

            log.debug(exc.msg)

