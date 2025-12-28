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
from typing import Tuple

from col import CircularQueue


class TestCircularQueue(unittest.TestCase):
    """Testing `CircularQueue` class."""

    def test_empty_queue_returns_none(self):
        """Dequeuing on an empty queue must return None."""

        sut = CircularQueue()

        result = sut.dequeue()

        self.assertIsNone(result)

    def test_enqueue_none_throws(self):
        """Enqueuing `None` is not supported."""

        sut = CircularQueue()

        with self.assertRaises(AssertionError):
            sut.enqueue(None)

    def test_enqueing_more_items_than_max_size_removes_oldest_item(self):
        """Enqueuing more items than the maximum size configured will overwrite older items."""

        expected_item = "item2"
        expected_size = 3

        sut = CircularQueue(expected_size)

        result = sut.enqueue("item1")
        result = sut.enqueue(expected_item)
        result = sut.enqueue("item3")
        result = sut.enqueue("item4")

        self.assertEqual(expected_size, len(sut))

        result = sut.dequeue()

        self.assertEqual(expected_item, result)

    def test_has_items_succeeds(self):
        """has_items returns true on non-empty queue."""

        sut = CircularQueue()

        self.assertFalse(sut.has_items)

        sut.enqueue("arbitrary-item")

        self.assertTrue(sut.has_items)

        _ = sut.dequeue()

        self.assertFalse(sut.has_items)

    def test_dequeue_filter_with_match_all_succeeds(self):
        """Lambda on dequeuing will only return selected items."""

        expected_key = "arbitrary-key"
        expected_value = "arbitrary-value"

        sut = CircularQueue[Tuple[str, str]]()

        expected_count = 3
        for _ in range(expected_count):
            sut.enqueue((expected_key, expected_value))

        result = sut.dequeue_filter(lambda e: True)

        self.assertEqual(expected_count, len(result))
        self.assertFalse(sut.has_items)

    def test_dequeue_filter_with_match_nothing_succeeds(self):
        """Lambda on dequeuing will only return selected items."""

        expected_key = "arbitrary-key"
        expected_value = "arbitrary-value"

        sut = CircularQueue[Tuple[str, str]]()

        expected_count = 3
        for _ in range(expected_count):
            sut.enqueue((expected_key, expected_value))

        self.assertEqual(expected_count, len(sut))

        result = sut.dequeue_filter(lambda e: False)

        self.assertEqual(expected_count, len(sut))

        self.assertEqual(0, len(result))

    def test_dequeue_filter_with_match_succeeds(self):
        """Lambda on dequeuing will only return selected items."""

        expected_key = "expected-key"
        expected_value = "expected-value"

        sut = CircularQueue[Tuple[str, str]]()

        expected_count = 3
        for _ in range(expected_count):
            sut.enqueue(("arbitrary-key", "arbitrary-value"))

        sut.enqueue((expected_key, expected_value))

        result = sut.dequeue_filter(lambda e: e[0] == expected_key)

        self.assertEqual(expected_count, len(sut))

        self.assertEqual(1, len(result))
        self.assertEqual(expected_key, result[0][0])
        self.assertEqual(expected_value, result[0][1])
