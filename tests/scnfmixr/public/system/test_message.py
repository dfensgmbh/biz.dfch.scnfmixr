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

"""Module test_message."""

from __future__ import annotations
import unittest

from biz.dfch.scnfmixr.public.system import MessagePriority

from biz.dfch.scnfmixr.public.system.message_medium import Message
from biz.dfch.scnfmixr.public.system.message_high import NotificationHigh
from biz.dfch.scnfmixr.public.system.message_medium import NotificationMedium
from biz.dfch.scnfmixr.public.system.message_low import NotificationLow


class TestMessage(unittest.TestCase):
    """Class message types."""

    @staticmethod
    def get_fqcn(_type: type) -> str:
        """Returns the full qualified class name."""
        return f"{type(_type).__module__}.{type(_type).__qualname__}"

    class ArbitraryMessage(Message):
        """Priority Medium."""

        description: str

        def __init__(self, description: str):
            super().__init__()

            assert description and description.strip()

            self.description = description

    class ArbitraryMessageHigh(NotificationHigh):
        """Priority High."""

        description: str

        def __init__(self, description: str):
            super().__init__()

            assert description and description.strip()

            self.description = description

    class ArbitraryMessageMedium(NotificationMedium):
        """Priority Medium."""

        description: str

        def __init__(self, description: str):
            super().__init__()

            assert description and description.strip()

            self.description = description

    class ArbitraryMessageLow(NotificationLow):
        """Priority Low."""

        description: str

        def __init__(self, description: str):
            super().__init__()

            assert description and description.strip()

            self.description = description

    def test_message(self):
        """Testing standard message."""

        expected_priority = MessagePriority.DEFAULT
        expected_description = "arbitrary-description"

        sut = TestMessage.ArbitraryMessage(expected_description)

        self.assertIsNotNone(sut)

        result = sut.name
        self.assertEqual(TestMessage.get_fqcn(sut), result)

        self.assertEqual(expected_priority, sut.priority)
        self.assertEqual(expected_description, sut.description)

    def test_message_high(self):
        """Testing high priority message."""

        expected_priority = MessagePriority.HIGH
        expected_description = "arbitrary-description"

        sut = TestMessage.ArbitraryMessageHigh(expected_description)

        self.assertIsNotNone(sut)

        result = sut.name
        self.assertEqual(TestMessage.get_fqcn(sut), result)

        self.assertEqual(expected_priority, sut.priority)
        self.assertEqual(expected_description, sut.description)

    def test_message_medium(self):
        """Testing medium priority message."""

        expected_priority = MessagePriority.MEDIUM
        expected_description = "arbitrary-description"

        sut = TestMessage.ArbitraryMessageMedium(expected_description)

        self.assertIsNotNone(sut)

        result = sut.name
        self.assertEqual(TestMessage.get_fqcn(sut), result)

        self.assertEqual(expected_priority, sut.priority)
        self.assertEqual(expected_description, sut.description)

    def test_message_low(self):
        """Testing high priority message."""

        expected_priority = MessagePriority.LOW
        expected_description = "arbitrary-description"

        sut = TestMessage.ArbitraryMessageLow(expected_description)

        self.assertIsNotNone(sut)

        result = sut.name
        self.assertEqual(TestMessage.get_fqcn(sut), result)

        self.assertEqual(expected_priority, sut.priority)
        self.assertEqual(expected_description, sut.description)


if __name__ == "__main__":
    unittest.main()
