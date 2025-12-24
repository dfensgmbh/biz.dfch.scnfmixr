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

"""Module test_message_queue."""

from __future__ import annotations
import unittest
from threading import Event

from biz.dfch.scnfmixr.public.system import Message
from biz.dfch.scnfmixr.public.system import MessageBase
from biz.dfch.scnfmixr.public.system import NotificationHigh
from biz.dfch.scnfmixr.public.system import NotificationMedium
from biz.dfch.scnfmixr.public.system import NotificationLow
from biz.dfch.scnfmixr.public.system import MessagePriority

from biz.dfch.scnfmixr.system.message_queue import MessageQueue


class TestMessageQueueT(unittest.TestCase):
    """Class testing template."""

    class ArbitraryMessage1(Message):
        """Priority Medium."""

    class ArbitraryMessage2(Message):
        """Priority Medium."""

    class ArbitraryMessageHigh(NotificationHigh):
        """Priority High."""

        description: str

    class ArbitraryMessageMedium(NotificationMedium):
        """Priority Medium."""

    class ArbitraryMessageLow(NotificationLow):
        """Priority Low."""

    def _on_event(self, message: MessageBase):
        """Event handler."""

        assert message and isinstance(message, MessageBase)

        print(f"type: '{type(message)}; "
              f"name: '{message.name}'; "
              f"priority: '{message.priority}'")

    def test_calling_ctor_throws(self):
        """Calling the ctor directly throws."""

        with self.assertRaises(AssertionError):
            _ = MessageQueue()

    def test_factory_returns_singleton(self):
        """Calling factory twice returns same instance."""

        sut1 = MessageQueue.Factory.get()
        sut2 = MessageQueue.Factory.get()

        self.assertEqual(sut1, sut2)

    def test_register_succeeds(self):
        """Registering action returns is_registered == true."""

        sut = MessageQueue.Factory.get()

        action = self._on_event

        result = sut.is_registered(action)
        self.assertFalse(result)

        result = sut.register(action)
        self.assertTrue(result)

        result = sut.is_registered(action)
        self.assertTrue(result)

        result = sut.register(action)
        self.assertFalse(result)

    def test_unregister_succeeds(self):
        """Unregistering action returns is_registered == true."""

        sut = MessageQueue.Factory.get()

        action = self._on_event

        result = sut.unregister(action)
        self.assertFalse(result)

        result = sut.is_registered(action)
        self.assertFalse(result)

        result = sut.register(action)
        self.assertTrue(result)

        result = sut.is_registered(action)
        self.assertTrue(result)

        result = sut.unregister(action)
        self.assertTrue(result)

        result = sut.is_registered(action)
        self.assertFalse(result)

        result = sut.unregister(action)
        self.assertFalse(result)

    class EventHandler:
        """EventReceive"""

        signal: Event
        messages: list[MessageBase]

        def __init__(self):
            self.messages = []
            self.signal = Event()

        def on_any_event_single_message_add_to_list(self, message: MessageBase):
            """Event handler."""

            assert message and isinstance(message, MessageBase)

            self.messages.append(message)

            if 1 == len(self.messages):
                self.signal.set()

        def on_any_event_two_messages_add_to_list(self, message: MessageBase):
            """Event handler."""

            assert message and isinstance(message, MessageBase)

            self.messages.append(message)

            if 2 == len(self.messages):
                self.signal.set()

    def test_callback_succeeds(self) -> None:
        """Testing callback."""

        message = TestMessageQueueT.ArbitraryMessage1()
        handler = TestMessageQueueT.EventHandler()

        sut: MessageQueue
        sut = MessageQueue.Factory.get()

        sut.register(handler.on_any_event_single_message_add_to_list)

        sut.publish(message)

        handler.signal.wait(5)

        self.assertEqual(1, len(handler.messages))

    def test_prioritising_messages_succeeds(self) -> None:
        """HIGH priority messages are dispatched first."""

        message_default = TestMessageQueueT.ArbitraryMessage1()
        message_high = TestMessageQueueT.ArbitraryMessageHigh()
        handler = TestMessageQueueT.EventHandler()

        sut: MessageQueue
        sut = MessageQueue.Factory.get()

        sut.register(handler.on_any_event_two_messages_add_to_list)

        sut.publish([message_default, message_high])

        handler.signal.wait(5)

        self.assertEqual(2, len(handler.messages))
        self.assertEqual(MessagePriority.HIGH, handler.messages[0].priority)
        self.assertEqual(MessagePriority.DEFAULT, handler.messages[1].priority)

    def test_enqueue_first_succeeds(self) -> None:
        """Enqueue at top of queue succeeds."""

        message1 = TestMessageQueueT.ArbitraryMessage1()
        message2 = TestMessageQueueT.ArbitraryMessage2()
        handler = TestMessageQueueT.EventHandler()

        sut: MessageQueue
        sut = MessageQueue.Factory.get()

        sut.register(handler.on_any_event_two_messages_add_to_list)

        sut.publish(message1)
        sut.publish_first(message2)

        handler.signal.wait(5)

        self.assertEqual(2, len(handler.messages))
        self.assertEqual(message2, handler.messages[0])
        self.assertEqual(message1, handler.messages[1])


if __name__ == "__main__":
    unittest.main()
