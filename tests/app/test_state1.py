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

from enum import Enum
import unittest


class TestState1(unittest.TestCase):
    """Testing State1 as part of the state machine."""

    class InfoStart(Enum):
        """State start info."""
        STATE1 = True

    class InfoEnd(Enum):
        """State end info."""
        STATE1 = True

    def test2(self):
        pass

    def test(self):
        """Arbitrary test."""

        sut = State1(TestState1.InfoStart.STATE1, TestState1.InfoEnd.STATE1)

        self.assertIsNotNone(sut)
        self.assertEqual(0, len(sut.transitions))


# if __name__ == "__main__":
#     unittest.main()
