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
