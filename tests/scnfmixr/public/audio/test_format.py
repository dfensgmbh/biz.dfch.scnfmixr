# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

# pylint: disable=C0115
# pylint: disable=C0116

"""test_format"""

import unittest

from biz.dfch.scnfmixr.public.audio import Format


class TestFormat(unittest.TestCase):

    def test_value_from_intenum(self):

        expected = 16

        result = Format.S16_LE.get_bit_depth()

        self.assertEqual(expected, result)
        self.assertEqual(expected, result.value)
