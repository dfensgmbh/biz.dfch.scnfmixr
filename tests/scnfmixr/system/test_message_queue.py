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

"""Module test_message_queue."""

from __future__ import annotations
import unittest
from threading import Event

from biz.dfch.scnfmixr.public.system import Message
from biz.dfch.scnfmixr.public.system import MessageBase
from biz.dfch.scnfmixr.public.system import MessageHigh
from biz.dfch.scnfmixr.public.system import MessageMedium
from biz.dfch.scnfmixr.public.system import MessageLow
from biz.dfch.scnfmixr.public.system import MessagePriority

from biz.dfch.scnfmixr.system.message_queue import MessageQueueT


class TestMessageQueueT(unittest.TestCase):
    """Class testing template."""

    class ArbitraryMessage(Message):
        """Priority Medium."""

    class ArbitraryMessageHigh(MessageHigh):
        """Priority High."""

        description: str

    class ArbitraryMessageMedium(MessageMedium):
        """Priority Medium."""

    class ArbitraryMessageLow(MessageLow):
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
            _ = MessageQueueT[MessageBase]()

    def test_factory_returns_singleton(self):
        """Calling factory twice returns same instance."""

        sut1 = MessageQueueT[MessageBase].Factory.get()
        sut2 = MessageQueueT[MessageBase].Factory.get()

        self.assertEqual(sut1, sut2)

    def test_register_succeeds(self):
        """Registering action returns is_registered == true."""

        sut = MessageQueueT[MessageBase].Factory.get()

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

        sut = MessageQueueT[MessageBase].Factory.get()

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

        message = TestMessageQueueT.ArbitraryMessage()
        handler = TestMessageQueueT.EventHandler()

        sut: MessageQueueT[MessageBase]
        sut = MessageQueueT[MessageBase].Factory.get()

        sut.register(handler.on_any_event_single_message_add_to_list)

        sut.publish(message)

        handler.signal.wait(5)

        self.assertEqual(1, len(handler.messages))

    def test_prioritising_messages_succeeds(self) -> None:
        """HIGH priority messages are dispatched first."""

        message_default = TestMessageQueueT.ArbitraryMessage()
        message_high = TestMessageQueueT.ArbitraryMessageHigh()
        handler = TestMessageQueueT.EventHandler()

        sut: MessageQueueT[MessageBase]
        sut = MessageQueueT[MessageBase].Factory.get()

        sut.register(handler.on_any_event_two_messages_add_to_list)

        sut.publish([message_default, message_high])

        handler.signal.wait(5)

        self.assertEqual(2, len(handler.messages))
        self.assertEqual(MessagePriority.HIGH, handler.messages[0].priority)
        self.assertEqual(MessagePriority.DEFAULT, handler.messages[1].priority)


if __name__ == "__main__":
    unittest.main()
