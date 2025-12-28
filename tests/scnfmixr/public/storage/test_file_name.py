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

"""Module test_file_name."""

# pylint: disable=C0112,C0116
# mypy: disable-error-code=annotation-unchecked

from datetime import datetime
import tempfile
import unittest

from biz.dfch.scnfmixr.public.storage import FileName
from biz.dfch.scnfmixr.public.audio import FileFormat


class TestFileName(unittest.TestCase):
    """TestFileName."""

    def test_is_valid_file_name_succeeds(self):

        dt = datetime(
            year=1927,
            month=3,
            day=27,
            hour=00,
            minute=8,
            second=15
        )

        sut = FileName(
            path_name=tempfile.gettempdir(),
            base_name="12345678",
            dt=dt,
            suffix="123",
            dash="-",
            separator="---",
            extension=FileFormat.MP3
        )

        result = sut.filename

        self.assertTrue(FileName.is_valid_filename(result), result)

    def test_is_valid_file_name_with_invalid_base_fails(self):

        dt = datetime(
            year=1927,
            month=3,
            day=27,
            hour=00,
            minute=8,
            second=15
        )

        sut = FileName(
            path_name=tempfile.gettempdir(),
            base_name="invalid",
            dt=dt,
            suffix="123",
            dash="-",
            separator="---",
            extension=FileFormat.MP3
        )

        result = sut.filename

        self.assertFalse(FileName.is_valid_filename(result), result)

    def test_is_valid_file_name_with_invalid_suffix_fails(self):

        dt = datetime(
            year=1927,
            month=3,
            day=27,
            hour=00,
            minute=8,
            second=15
        )

        sut = FileName(
            path_name=tempfile.gettempdir(),
            base_name="12345678",
            dt=dt,
            suffix="too-long",
            dash="-",
            separator="---",
            extension=FileFormat.MP3
        )

        result = sut.filename

        self.assertFalse(FileName.is_valid_filename(result), result)
