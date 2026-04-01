# Copyright (c) 2024 - 2026 d-fens GmbH, http://d-fens.ch
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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0212

import datetime
from datetime import timedelta
import time
import unittest

from biz.dfch.scnfmixr.date_time_name_input import DateTimeNameInput
from biz.dfch.scnfmixr.public.system.system_time import SystemTime


class TestDateTimeNameInput(unittest.TestCase):
    """Testing DateTimeNameInput."""

    def test_adding_valid_input_to_date_succeeds(self):
        """Adding a valid character to the date succeeds."""

        sut = DateTimeNameInput()

        sut.add_to_date("1")

        self.assertEqual("1", sut._date_string)

    def test_adding_invalid_input_to_date_succeeds(self):
        """Adding a invalid character to the date succeeds."""

        sut = DateTimeNameInput()

        with self.assertRaises(AssertionError):
            sut.add_to_date("D")

    def test_adding_valid_input_to_time_succeeds(self):
        """Adding a valid character to the time succeeds."""

        sut = DateTimeNameInput()

        sut.add_to_time("1")

        self.assertEqual("1", sut._time_string)

    def test_adding_invalid_input_to_time_succeeds(self):
        """Adding a invalid character to the time succeeds."""

        sut = DateTimeNameInput()

        with self.assertRaises(AssertionError):
            sut.add_to_time("D")

    def test_adding_valid_time_to_time_succeeds(self):
        """Adding a valid time to the time succeeds."""

        sut = DateTimeNameInput()

        sut.add_to_time("1")
        sut.add_to_time("2")
        sut.add_to_time("3")
        sut.add_to_time("4")

        self.assertEqual("1234", sut._time_string)
        self.assertFalse(sut.is_valid_time)

        sut.add_to_time("!")
        self.assertTrue(sut.is_valid_time)

        self.assertEqual(datetime.time(12, 34), sut.get_time())

    def test_sending_backspace_removes_char_from_time(self):
        """Sending a backspace removes a character from time string."""

        sut = DateTimeNameInput()

        sut.add_to_time("1")
        self.assertEqual("1", sut._time_string)
        sut.add_to_time("2")
        self.assertEqual("12", sut._time_string)
        sut.add_to_time("3")
        self.assertEqual("123", sut._time_string)

        self.assertFalse(sut.is_valid_time)

        sut.add_to_time(sut._EVENT_BACKSPACE)

        self.assertEqual("12", sut._time_string)
        self.assertFalse(sut.is_valid_time)

    def test_adding_valid_date_to_date_succeeds(self):
        """Adding a valid date to the date succeeds."""

        sut = DateTimeNameInput()

        sut.add_to_date("1")
        self.assertEqual("1", sut._date_string)
        sut.add_to_date("9")
        self.assertEqual("19", sut._date_string)
        sut.add_to_date("2")
        self.assertEqual("192", sut._date_string)
        sut.add_to_date("7")
        self.assertEqual("1927", sut._date_string)
        sut.add_to_date("0")
        self.assertEqual("19270", sut._date_string)
        sut.add_to_date("3")
        self.assertEqual("192703", sut._date_string)
        sut.add_to_date("2")
        self.assertEqual("1927032", sut._date_string)
        sut.add_to_date("7")
        self.assertEqual("19270327", sut._date_string)

        self.assertFalse(sut.is_valid_date)

        sut.add_to_date("!")

        self.assertTrue(sut.is_valid_date)

        self.assertEqual(datetime.date(1927, 3, 27), sut.get_date())

    def test_adding_valid_name_to_name_succeeds(self):
        """Adding a valid name to the name succeeds."""

        sut = DateTimeNameInput()

        sut.add_to_name("1")
        self.assertEqual("1", sut._name_string)
        sut.add_to_name("9")
        self.assertEqual("19", sut._name_string)
        sut.add_to_name("2")
        self.assertEqual("192", sut._name_string)
        sut.add_to_name("7")
        self.assertEqual("1927", sut._name_string)
        sut.add_to_name("0")
        self.assertEqual("19270", sut._name_string)
        sut.add_to_name("3")
        self.assertEqual("192703", sut._name_string)
        sut.add_to_name("2")
        self.assertEqual("1927032", sut._name_string)
        sut.add_to_name("7")
        self.assertEqual("19270327", sut._name_string)

        self.assertFalse(sut.is_valid_name)

        sut.add_to_name("!")

        self.assertTrue(sut.is_valid_name)

        self.assertEqual("19270327", sut.get_name())

    def test_later_1(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=1, hours=1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertIsNone(result)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertTrue(is_almost_equal, (expected, result))

    def test_later_2(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=0, hours=1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertEqual(result, None)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertTrue(is_almost_equal, (expected, result))

    def test_earlier_1(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=-1, hours=-1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertIsNone(result)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertTrue(is_almost_equal, (expected, result))

    def test_earlier_2(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=-1, hours=1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertIsNone(result)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertTrue(is_almost_equal, (expected, result))

    def test_earlier_3(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=0, hours=-1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertIsNone(result)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertTrue(is_almost_equal, (expected, result))

    def test_later_fails(self):

        # Real current system time.
        now = datetime.datetime.now()
        expected = now + timedelta(days=1, hours=1)
        st = SystemTime.Factory.get()

        sut = DateTimeNameInput()

        # Get and set date.
        result = sut.get_date()
        self.assertIsNone(result)

        sut.set_date(expected.date())

        result = sut.get_date()
        print(result)
        result = st.now()
        print(result)

        # Get and set time.
        result = sut.get_time()
        self.assertIsNone(result)

        sut.set_time(expected.time())

        time.sleep(1.1)

        result = sut.get_time()
        print(result)
        result = st.now()
        print(result)

        is_almost_equal = abs(expected - result) <= timedelta(seconds=1)

        self.assertFalse(is_almost_equal, (expected, result))
