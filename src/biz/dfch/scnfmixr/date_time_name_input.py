# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
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

"""Module date_time_name_input."""

import datetime
import random
import string

from .public.system import SystemTime


class DateTimeNameInput():
    """Processes and represents date, time and name input."""

    DATE_LENGTH = 8
    TIME_LENGTH = 4
    NAME_LENGTH = 8

    _EVENT_BACKSPACE = "£"
    _EVENT_ENTER = "!"

    _date: datetime.date
    _time: datetime.time
    _name: str
    _is_valid_date: bool
    _is_valid_time: bool
    _is_valid_name: bool
    _date_string: str
    _time_string: str
    _name_string: str

    def __init__(self):

        self._date = None
        self._time = None
        self._name = None
        self._date_string = ""
        self._time_string = ""
        self._name_string = ""

        self.reset()

    def __str__(self) -> str:
        result = {
            "date": self.get_date(),
            "time": self.get_time(),
            "name": self.get_name(),
        }

        return str(result)

    def get_datetime(self) -> datetime:
        """Returns the date and time."""
        return datetime.datetime.combine(self._date, self._time)

    def get_date(self) -> datetime.date:
        """Returns the date."""
        return self._date

    def set_date(self, value: datetime.date) -> None:
        """Sets the date."""

        assert value is not None and isinstance(value, datetime.date)

        self._date_string = ""
        self._date = value

        st = SystemTime.Factory.get()
        st.set(datetime.datetime.combine(value, st.now().time()))

    def get_time(self) -> datetime.time:
        """Returns the time."""
        return self._time

    def set_time(self, value: datetime.time) -> None:
        """Sets the time."""

        assert value is not None and isinstance(value, datetime.time)

        self._time_string = ""
        self._time = value

        st = SystemTime.Factory.get()
        st.set(datetime.datetime.combine(st.now().date(), value))

    def get_name(self) -> datetime.time:
        """Returns the name."""
        return self._name

    def set_name(self, value: str) -> None:
        """Sets the name."""

        assert value and value.strip()

        self._name_string = ""
        self._name = value

    def set_pseudo_random_name(self) -> None:
        """Sets a pseudo random name."""

        pool = string.digits
        value = ''.join(random.choices(pool, k=8))

        self._name = value

    @property
    def is_valid_date(self) -> bool:
        """Determines whether the date is a valid date."""
        return bool(self._date)

    @property
    def is_valid_time(self) -> bool:
        """Determines whether the time is a valid time."""
        return bool(self._time)

    @property
    def is_valid_name(self) -> bool:
        """Determines whether the name is a valid name."""
        return bool(self._name)

    def reset(self) -> None:
        """Resets all data."""

        self._date = None
        self._time = None
        self._name = None
        self._date_string = ""
        self._time_string = ""
        self._name_string = ""

    def _validate_date(self, value: str) -> datetime.date | None:
        try:
            assert value and value.strip()

            year = int(value[0:4])
            month = int(value[4:6])
            day = int(value[6:8])

            result = datetime.date(year, month, day)
            return result
        except Exception:  # pylint: disable=W0718
            return None

    def _validate_time(self, value: str) -> datetime.time | None:
        try:
            assert value and value.strip()

            hour = int(value[0:2])
            minute = int(value[2:4])

            result = datetime.time(hour, minute)
            return result
        except Exception:  # pylint: disable=W0718
            return None

    def _validate_name(self, value: str) -> str | None:
        try:
            assert value and value.strip()
            assert self.NAME_LENGTH == len(value)

            result = value
            return result
        except Exception:  # pylint: disable=W0718
            return None

    def add_to_date(self, value: str) -> bool:
        """Adds digits to a date string."""

        assert not self.is_valid_date
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._date_string is not None and self._date_string.strip():
                self._date_string = self._date_string[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_date(self._date_string)
            self._date_string = ""
            if result is None:
                return True

            self.set_date(result)
            return True

        digit = int(value)
        self._date_string = f"{self._date_string}{digit}"
        self._date = None

        return True

    def add_to_time(self, value: str) -> bool:
        """Adds digits to a time string."""

        assert not self.is_valid_time
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._time_string is not None and self._time_string.strip():
                self._time_string = self._time_string[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_time(self._time_string)
            self._time_string = ""
            if result is None:
                return True

            self.set_time(result)
            return True

        digit = int(value)
        self._time_string = f"{self._time_string}{digit}"
        self._time = None

        return True

    def add_to_name(self, value: str) -> bool:
        """Adds digits to a name string."""

        assert not self.is_valid_name
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._name_string is not None and self._name_string.strip():
                self._name_string = self._name_string[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_name(self._name_string)
            self._name_string = ""
            if result is None:
                return True

            self._name = result
            return True

        digit = int(value)
        self._name_string = f"{self._name_string}{digit}"
        self._name = None

        return True
