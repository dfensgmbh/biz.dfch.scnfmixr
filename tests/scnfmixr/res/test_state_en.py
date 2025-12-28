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

"""Module test_state_en."""

# pylint: disable=C0112,C0116
# mypy: disable-error-code=annotation-unchecked

import unittest

from biz.dfch.scnfmixr.core.state_event import StateEvent

from prep.snd.state_event_en import StateEventEn


class TestStateEventEn(unittest.TestCase):
    """Testing StateEvent definitions for EN."""

    def test_missing_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key in StateEvent:

            if key not in StateEventEn:
                result.append(key.name)

        self.assertEqual(0, len(result), result)

    def test_extra_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key in StateEventEn:

            if key not in StateEvent:
                result.append(key.name)

        self.assertEqual(0, len(result), result)

    def test_empty_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key, value in StateEventEn.items():

            if 1 == len(value):
                result.append(key.name)

        self.assertEqual(0, len(result), result)
