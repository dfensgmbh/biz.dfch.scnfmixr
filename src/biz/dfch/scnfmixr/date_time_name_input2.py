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

"""Module date_time_name_input2."""

import datetime


# pylint: disable=R0902
class DateTimeNameInput2():
    """Processes and represents date, time and name input.

    Alternative handling w/o ENTER and BACKSPACE."""

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

        self._date = None
        self._time = None
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
        return datetime.datetime(
            self._date.year, self._date.month, self._date.day,
            self._time.hour, self._time.minute)

    def get_date(self) -> datetime.date:
        """Returns the date."""
        return self._date

    def get_time(self) -> datetime.time:
        """Returns the time."""
        return self._time

    def get_name(self) -> datetime.time:
        """Returns the name."""
        return self._name

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
        self._datestring = ""
        self._timestring = ""
        self._namestring = ""

    def _validate_date(self, year: int, month: int, day: int) -> bool:
        try:
            datetime.date(year, month, day)
            return True
        except Exception:  # pylint: disable=W0718
            return False

    def _validate_time(self, hour: int, minute: int) -> bool:
        try:
            datetime.time(hour, minute)
            return True
        except Exception:  # pylint: disable=W0718
            return False

    def add_to_date(self, value: str) -> bool:
        """Adds digits to a date string."""

        assert not self._is_valid_date
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._datestring is not None and self._datestring.strip():
                self._datestring = self._datestring[:-1]
            return True

        result = False
        digit = int(value)
        idx = len(self._datestring)
        match idx:
            # Year YYYY.
            case _ if 0 <= idx <= 3:
                result = True
            # Month MM[0].
            case 4:
                result = 0 <= digit <= 1
            # Month MM[1].
            case 5:
                yyyy = int(self._datestring[0:4])
                mm = int(self._datestring[idx - 1]) * 10 + digit
                result = self._validate_date(yyyy, mm, 1)
            # Day dd[0].
            case 6:
                yyyy = int(self._datestring[0:4])
                mm = int(self._datestring[4:6])
                dd = digit * 10 + 1
                result = self._validate_date(yyyy, mm, dd)
            # Day dd[1].
            case 7:
                yyyy = int(self._datestring[0:4])
                mm = int(self._datestring[4:6])
                dd = int(self._datestring[idx - 1]) * 10 + digit
                result = self._validate_date(yyyy, mm, dd)

        if not result:
            return result

        self._datestring = f"{self._datestring}{digit}"

        if not len(self._datestring) == self.DATE_LENGTH:
            return result

        yyyy = int(self._datestring[0:4])
        mm = int(self._datestring[4:6])
        dd = int(self._datestring[6:8])

        result = self._validate_date(yyyy, mm, dd)
        if result:
            self._is_valid_date = result
            self._date = datetime.date(yyyy, mm, dd)

        return result

    def add_to_time(self, value: str) -> bool:
        """Adds digits to a time string."""

        assert not self._is_valid_time
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._timestring is not None and self._timestring.strip():
                self._timestring = self._timestring[:-1]
            return True

        result = False
        digit = int(value)
        idx = len(self._timestring)
        match idx:
            # Hour HH[0]
            case 0:
                result = 0 <= digit <= 2
            # Hour HH[1]
            case 1:
                hh = int(self._timestring[idx - 1]) * 10 + digit
                result = self._validate_time(hh, 0)
            # Minute mm[0]
            case 2:
                result = 0 <= digit <= 5
            # Minute mm[1]
            case 3:
                result = 0 <= digit <= 9

        if not result:
            return result

        self._timestring = f"{self._timestring}{digit}"

        if not len(self._timestring) == self.TIME_LENGTH:
            return result

        hh = int(self._timestring[0:2])
        mm = int(self._timestring[2:4])
        result = self._validate_time(hh, mm)

        if result:
            self._is_valid_time = result
            self._time = datetime.time(hh, mm)

        return result

    def add_to_name(self, value: str) -> bool:
        """Adds digits to a name string."""

        assert not self._is_valid_name
        assert value and value.strip()
        assert 1 == len(value)
        assert value.isdigit() or value in (
            self._EVENT_BACKSPACE, self._EVENT_ENTER)

        if self._EVENT_BACKSPACE == value:
            if self._namestring is not None and self._namestring.strip():
                self._namestring = self._namestring[:-1]
            return True

        digit = int(value)
        self._namestring = f"{self._namestring}{digit}"

        result = len(self._namestring) == self.NAME_LENGTH
        if not result:
            return result

        self._name = self._namestring
        self._is_valid_name = result
        return result
