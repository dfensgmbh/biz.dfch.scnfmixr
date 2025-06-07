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

from col import CircularQueue


class TestCircularQueue(unittest.TestCase):

    def test_empty_queue_returns_none(self):

        sut = CircularQueue()

        result = sut.dequeue()

        self.assertIsNone(result)

    def test_enqueue_none_throws(self):

        sut = CircularQueue()

        with self.assertRaises(AssertionError):
            sut.enqueue(None)

    def test_enqueing_more_items_than_max_size_removes_oldest_item(self):

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

        sut = CircularQueue(3)

        # self.assertFalse(sut.has_items)

        _ = sut.enqueue("arbitrary-item")

        self.assertTrue(sut.has_items)

        _ = sut.dequeue()
        print(f"len: {len(sut)}")

        self.assertFalse(sut.has_items)
