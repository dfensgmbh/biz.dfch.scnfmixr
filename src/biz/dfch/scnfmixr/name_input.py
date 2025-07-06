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

"""Module name_input."""

from datetime import date, datetime, time


class DateTimeNameInput():
    """Processes and represents date, time and name input."""

    DATE_LENGTH = 8
    TIME_LENGTH = 4
    NAME_LENGTH = 8

    NAME_DEFAULT = "12345678"

    def __init__(self):
        now = datetime.now()
        self._date: date = now.date()
        self._time: time = now.time()
        self._name = self.NAME_DEFAULT
        self._is_valid_date = False
        self._is_valid_time = False
        self._is_valid_name = False
        self._datestring = ""
        self._timestring = ""
        self._namestring = ""

        self.reset()

    @property
    def datetime(self) -> datetime:
        """Returns the recorded date and time."""
        return datetime(self._date.year, self._date.month, self._date.day,
                        self._time.hour, self._time.minute)

    @property
    def date(self) -> date:
        """Returns the recorded date."""
        return self._date

    @property
    def time(self) -> time:
        """Returns the recorded time."""
        return self._time

    @property
    def name(self) -> time:
        """Returns the recorded name."""
        return self._name

    @property
    def is_valid_date(self) -> bool:
        """Determines whether the recorded date is a valid date."""
        return self._is_valid_date

    @property
    def is_valid_time(self) -> bool:
        """Determines whether the recorded time is a valid time."""
        return self._is_valid_time

    @property
    def is_valid_name(self) -> bool:
        """Determines whether the recorded name is a valid name."""
        return self._is_valid_name

    def reset(self) -> None:
        """Resets all data."""

        now = datetime.now()
        self._date: date = now.date()
        self._time: time = now.time()
        self._name = self.NAME_DEFAULT
        self._is_valid_date = False
        self._is_valid_time = False
        self._is_valid_name = False
        self._datestring = ""
        self._timestring = ""
        self._namestring = ""

    def _vaidate_date(self, year: int, month: int, day: int) -> bool:
        try:
            date(year, month, day)
            return True
        except Exception:  # pylint: disable=W0718
            return False

    def _vaidate_time(self, hour: int, minute: int) -> bool:
        try:
            time(hour, minute)
            return True
        except Exception:  # pylint: disable=W0718
            return False

    def add_to_date(self, value: str) -> bool:
        """Adds digits to a date string."""

        assert not self._is_valid_date
        assert value and value.strip()
        assert 1 == len(value) and value.isdigit()

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
                result = self._vaidate_date(yyyy, mm, 1)
            # Day dd[0].
            case 6:
                yyyy = int(self._datestring[0:4])
                mm = int(self._datestring[4:6])
                dd = digit * 10 + 1
                result = self._vaidate_date(yyyy, mm, dd)
            # Day dd[1].
            case 7:
                yyyy = int(self._datestring[0:4])
                mm = int(self._datestring[4:6])
                dd = int(self._datestring[idx - 1]) * 10 + digit
                result = self._vaidate_date(yyyy, mm, dd)

        if not result:
            return result

        self._datestring = f"{self._datestring}{digit}"

        if not len(self._datestring) == self.DATE_LENGTH:
            return result

        yyyy = int(self._datestring[0:4])
        mm = int(self._datestring[4:6])
        dd = int(self._datestring[6:8])

        result = self._vaidate_date(yyyy, mm, dd)
        if result:
            self._is_valid_date = result
            self._date = date(yyyy, mm, dd)

        return result

    def add_to_time(self, value: str) -> bool:
        """Adds digits to a time string."""

        assert not self._is_valid_time
        assert value and value.strip()
        assert 1 == len(value) and value.isdigit()

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
                result = self._vaidate_time(hh, 0)
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
        result = self._vaidate_time(hh, mm)

        if result:
            self._is_valid_time = result
            self._time = time(hh, mm)

        return result

    def add_to_name(self, value: str) -> bool:
        """Adds digits to a name string."""

        assert not self._is_valid_name
        assert value and value.strip()
        assert 1 == len(value) and value.isdigit()

        digit = int(value)
        self._namestring = f"{self._namestring}{digit}"

        result = len(self._namestring) == self.NAME_LENGTH
        if not result:
            return result

        self._name = self._namestring
        self._is_valid_name = result
        return result
