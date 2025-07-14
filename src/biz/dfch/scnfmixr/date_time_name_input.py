# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

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

"""Module date_time_name_input."""

import datetime
import random
import string


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
    _datestring: str
    _timestring: str
    _namestring: str

    def __init__(self):

        self._date: datetime.date = None
        self._time: datetime.time = None
        self._name = None
        self._datestring = ""
        self._timestring = ""
        self._namestring = ""

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

        self._date = value

    def get_time(self) -> datetime.time:
        """Returns the time."""
        return self._time

    def set_time(self, value: datetime.time) -> None:
        """Sets the time."""

        assert value is not None and isinstance(value, datetime.time)

        self._time = value

    def get_name(self) -> datetime.time:
        """Returns the name."""
        return self._name

    def set_name(self, value: str) -> None:
        """Sets the name."""

        assert value and value.strip()

        self._name = value

    def set_pseudo_random_name(self) -> None:
        """Sets a pseudo random name."""

        pool = string.ascii_lowercase + string.digits
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

        self._date: datetime.date = None
        self._time: datetime.time = None
        self._name = None
        self._datestring = ""
        self._timestring = ""
        self._namestring = ""

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
            if self._datestring is not None and self._datestring.strip():
                self._datestring = self._datestring[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_date(self._datestring)
            self._datestring = ""
            if result is None:
                return True

            self._date = result
            return True

        digit = int(value)
        self._datestring = f"{self._datestring}{digit}"
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
            if self._timestring is not None and self._timestring.strip():
                self._timestring = self._timestring[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_time(self._timestring)
            self._timestring = ""
            if result is None:
                return True

            self._time = result
            return True

        digit = int(value)
        self._timestring = f"{self._timestring}{digit}"
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
            if self._namestring is not None and self._namestring.strip():
                self._namestring = self._namestring[:-1]
            return True

        if self._EVENT_ENTER == value:
            result = self._validate_name(self._namestring)
            self._namestring = ""
            if result is None:
                return True

            self._name = result
            return True

        digit = int(value)
        self._namestring = f"{self._namestring}{digit}"
        self._name = None

        return True
