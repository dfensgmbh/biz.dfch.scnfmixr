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

import importlib
import os
import unittest

from text import TextUtils


class TextUtilsTest(unittest.TestCase):

    def setUp(self):
        module_name = TextUtils.__module__
        module = importlib.import_module(module_name)
        self.existing_file = module.__file__

    def test_reading_non_existing_file_throws(self):
        with self.assertRaises(FileNotFoundError):
            TextUtils().read_first_line("something")

    def test_reading_existing_file_succeeds(self):
        result = TextUtils().read_first_line(os.path.join(self.existing_file))
        self.assertIsNotNone(result)
