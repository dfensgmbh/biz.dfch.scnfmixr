# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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
