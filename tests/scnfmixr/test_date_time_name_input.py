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
        self.assertEqual("1", sut._date_string)

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
        self.assertEqual("1", sut._time_string)

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

        self.assertEqual("1234", sut._time_string)
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
        self.assertEqual("1", sut._time_string)
        result = sut.add_to_time("2")
        self.assertTrue(result)
        self.assertEqual("12", sut._time_string)
        result = sut.add_to_time("3")
        self.assertTrue(result)
        self.assertEqual("123", sut._time_string)

        self.assertFalse(sut.is_valid_time)

        result = sut.add_to_time(sut._EVENT_BACKSPACE)

        self.assertEqual("12", sut._time_string)
        self.assertFalse(sut.is_valid_time)

    def test_adding_valid_date_to_date_succeeds(self):
        """Adding a valid date to the date succeeds."""

        sut = DateTimeNameInput()

        result = sut.add_to_date("1")
        self.assertTrue(result)
        self.assertEqual("1", sut._date_string)
        result = sut.add_to_date("9")
        self.assertTrue(result)
        self.assertEqual("19", sut._date_string)
        result = sut.add_to_date("2")
        self.assertTrue(result)
        self.assertEqual("192", sut._date_string)
        result = sut.add_to_date("7")
        self.assertTrue(result)
        self.assertEqual("1927", sut._date_string)
        result = sut.add_to_date("0")
        self.assertTrue(result)
        self.assertEqual("19270", sut._date_string)
        result = sut.add_to_date("3")
        self.assertTrue(result)
        self.assertEqual("192703", sut._date_string)
        result = sut.add_to_date("2")
        self.assertTrue(result)
        self.assertEqual("1927032", sut._date_string)
        result = sut.add_to_date("7")
        self.assertTrue(result)
        self.assertEqual("19270327", sut._date_string)

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
        self.assertEqual("1", sut._name_string)
        result = sut.add_to_name("9")
        self.assertTrue(result)
        self.assertEqual("19", sut._name_string)
        result = sut.add_to_name("2")
        self.assertTrue(result)
        self.assertEqual("192", sut._name_string)
        result = sut.add_to_name("7")
        self.assertTrue(result)
        self.assertEqual("1927", sut._name_string)
        result = sut.add_to_name("0")
        self.assertTrue(result)
        self.assertEqual("19270", sut._name_string)
        result = sut.add_to_name("3")
        self.assertTrue(result)
        self.assertEqual("192703", sut._name_string)
        result = sut.add_to_name("2")
        self.assertTrue(result)
        self.assertEqual("1927032", sut._name_string)
        result = sut.add_to_name("7")
        self.assertTrue(result)
        self.assertEqual("19270327", sut._name_string)

        self.assertFalse(sut.is_valid_name)

        result = sut.add_to_name("!")
        self.assertTrue(result)

        self.assertTrue(sut.is_valid_name)

        self.assertEqual("19270327", sut.get_name())
