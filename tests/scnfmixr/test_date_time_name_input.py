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

import datetime
import unittest

from biz.dfch.scnfmixr.date_time_name_input import DateTimeNameInput


class TestDateTimeNameInput(unittest.TestCase):
    """Testing DateTimeNameInput."""

    def test_adding_valid_input_to_date_succeeds(self):
        """Adding a valid character to the date succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_date("1")

        self.assertTrue(result)
        self.assertEqual("1", sut._datestring)

    def test_adding_invalid_input_to_date_succeeds(self):
        """Adding a invalid character to the date succeeds."""

        sut = DateTimeNameInput()

        with self.assertRaises(AssertionError):
            _ = sut.add_to_date("D")

    def test_adding_valid_input_to_time_succeeds(self):
        """Adding a valid character to the time succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_time("1")

        self.assertTrue(result)
        self.assertEqual("1", sut._timestring)

    def test_adding_invalid_input_to_time_succeeds(self):
        """Adding a invalid character to the time succeeds."""

        sut = DateTimeNameInput()

        with self.assertRaises(AssertionError):
            _ = sut.add_to_time("D")

    def test_adding_valid_time_to_time_succeeds(self):
        """Adding a valid time to the time succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_time("1")
        self.assertTrue(result)
        result = sut.add_to_time("2")
        self.assertTrue(result)
        result = sut.add_to_time("3")
        self.assertTrue(result)
        result = sut.add_to_time("4")
        self.assertTrue(result)

        self.assertEqual("1234", sut._timestring)
        self.assertFalse(sut.is_valid_time)

        result = sut.add_to_time("!")
        self.assertTrue(result)
        self.assertTrue(sut.is_valid_time)

        self.assertEqual(datetime.time(12, 34), sut.get_time())

    def test_sending_backspace_removes_char_from_time(self):
        """Sending a backspace removes a character from timestring."""

        sut = DateTimeNameInput()

        result = sut.add_to_time("1")
        self.assertTrue(result)
        self.assertEqual("1", sut._timestring)
        result = sut.add_to_time("2")
        self.assertTrue(result)
        self.assertEqual("12", sut._timestring)
        result = sut.add_to_time("3")
        self.assertTrue(result)
        self.assertEqual("123", sut._timestring)

        self.assertFalse(sut.is_valid_time)

        result = sut.add_to_time(sut._EVENT_BACKSPACE)

        self.assertEqual("12", sut._timestring)
        self.assertFalse(sut.is_valid_time)

    def test_adding_valid_date_to_date_succeeds(self):
        """Adding a valid date to the date succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_date("1")
        self.assertTrue(result)
        self.assertEqual("1", sut._datestring)
        result = sut.add_to_date("9")
        self.assertTrue(result)
        self.assertEqual("19", sut._datestring)
        result = sut.add_to_date("2")
        self.assertTrue(result)
        self.assertEqual("192", sut._datestring)
        result = sut.add_to_date("7")
        self.assertTrue(result)
        self.assertEqual("1927", sut._datestring)
        result = sut.add_to_date("0")
        self.assertTrue(result)
        self.assertEqual("19270", sut._datestring)
        result = sut.add_to_date("3")
        self.assertTrue(result)
        self.assertEqual("192703", sut._datestring)
        result = sut.add_to_date("2")
        self.assertTrue(result)
        self.assertEqual("1927032", sut._datestring)
        result = sut.add_to_date("7")
        self.assertTrue(result)
        self.assertEqual("19270327", sut._datestring)

        self.assertFalse(sut.is_valid_date)

        result = sut.add_to_date("!")
        self.assertTrue(result)

        self.assertTrue(sut.is_valid_date)

        self.assertEqual(datetime.date(1927, 3, 27), sut.get_date())

    def test_adding_valid_name_to_name_succeeds(self):
        """Adding a valid name to the name succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_name("1")
        self.assertTrue(result)
        self.assertEqual("1", sut._namestring)
        result = sut.add_to_name("9")
        self.assertTrue(result)
        self.assertEqual("19", sut._namestring)
        result = sut.add_to_name("2")
        self.assertTrue(result)
        self.assertEqual("192", sut._namestring)
        result = sut.add_to_name("7")
        self.assertTrue(result)
        self.assertEqual("1927", sut._namestring)
        result = sut.add_to_name("0")
        self.assertTrue(result)
        self.assertEqual("19270", sut._namestring)
        result = sut.add_to_name("3")
        self.assertTrue(result)
        self.assertEqual("192703", sut._namestring)
        result = sut.add_to_name("2")
        self.assertTrue(result)
        self.assertEqual("1927032", sut._namestring)
        result = sut.add_to_name("7")
        self.assertTrue(result)
        self.assertEqual("19270327", sut._namestring)

        self.assertFalse(sut.is_valid_name)

        result = sut.add_to_name("!")
        self.assertTrue(result)

        self.assertTrue(sut.is_valid_name)

        self.assertEqual("19270327", sut.get_name())

