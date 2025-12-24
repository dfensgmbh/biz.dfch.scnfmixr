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
