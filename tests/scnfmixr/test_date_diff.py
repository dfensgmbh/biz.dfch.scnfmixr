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

"""Module test_date_diff."""

import unittest
from datetime import datetime, timedelta
import string

from biz.dfch.logging import log


class TestDateDiff(unittest.TestCase):
    """Testing date diff for unique file name generation."""

    def map_number_to_char(self, value: int) -> str:
        """Maps a number to a char."""

        _NUMBER_MIN: int = 0
        _NUMBER_MAX: int = 59
        _NUMBER_TOTAL: int = _NUMBER_MAX + 1

        assert _NUMBER_MIN <= value <= _NUMBER_MAX

        chars = string.ascii_lowercase
        chars_count = len(chars)

        idx = int(value * chars_count / _NUMBER_TOTAL)

        result = chars[idx]

        return result

    def test_mapping_succeeds(self):
        """Maps all values to chars."""

        for i in range(0, 60):
            log.debug("%s: %s", i, self.map_number_to_char(i))

    def test_actual_after_now(self):
        """Testing something."""

        separator: str = "-"
        prefix: str = "arbitrary-prefix"
        case_id: str = "12345678"

        system_time: datetime = datetime(2025, 1, 1, 0, 0)
        actual_time: datetime = datetime(2025, 1, 1, 1, 0)
        delta: timedelta = actual_time - system_time

        now: datetime = datetime(2025, 1, 1, 12, 0)
        now_as_string = (now + delta).strftime("%Y%m%dT%H%M")
        # elapsed2: str = now.strftime("%Y-%m-%dT%H-%M-%S")
        elapsed2: str = self.map_number_to_char(now.second)

        # <prefix>-<case-id>-<dat_given:YYYY-MM-ddTHH-mm>-<unique_id:YYYYMMddHHmm>

        log.debug(now_as_string)

        result = f"{prefix}{3*separator}{case_id}{3*separator}" \
            f"{now_as_string}{3*separator}{elapsed2}"
        log.debug("now + delta '%s'", result)

    def test_actual_before_now(self):
        """Testing something."""

        separator: str = "-"
        prefix: str = "arbitrary-prefix"
        case_id: str = "12345678"

        system_time: datetime = datetime(2025, 1, 1, 0, 0)
        actual_time: datetime = datetime(2024, 12, 31, 23, 0)
        delta: timedelta = actual_time - system_time

        now: datetime = datetime(2025, 1, 1, 12, 0)
        now_as_string = (now + delta).strftime("%Y%m%dT%H%M")
        # elapsed2: str = now.strftime("%Y-%m-%dT%H-%M-%S")
        elapsed2: str = self.map_number_to_char(now.second)

        # <prefix>-<case-id>-<dat_given:YYYY-MM-ddTHH-mm>-<unique_id:YYYYMMddHHmm>

        log.debug(now_as_string)

        result = f"{prefix}{3*separator}{case_id}{3*separator}" \
            f"{now_as_string}{3*separator}{elapsed2}"
        log.debug("now + delta '%s'", result)

    def test_actual_match_now(self):
        """Testing something."""

        separator: str = "-"
        prefix: str = "arbitrary-prefix"
        case_id: str = "12345678"

        system_time: datetime = datetime(2025, 1, 1, 0, 0)
        actual_time: datetime = datetime(2025, 1, 1, 0, 0)
        delta: timedelta = actual_time - system_time

        now: datetime = datetime(2025, 1, 1, 12, 0)
        now_as_string = (now + delta).strftime("%Y%m%dT%H%M")
        # elapsed2: str = now.strftime("%Y-%m-%dT%H-%M-%S")
        elapsed2: str = self.map_number_to_char(now.second)

        # <prefix>-<case-id>-<dat_given:YYYY-MM-ddTHH-mm>-<unique_id:YYYYMMddHHmm>

        log.debug(now_as_string)

        result = f"{prefix}{3*separator}{case_id}{3*separator}" \
            f"{now_as_string}{3*separator}{elapsed2}"
        log.debug("now + delta '%s'", result)
