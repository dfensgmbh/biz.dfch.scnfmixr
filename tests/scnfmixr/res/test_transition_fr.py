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

"""Module test_transition_fr."""

# pylint: disable=C0112,C0116
# mypy: disable-error-code=annotation-unchecked

import unittest

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent

from prep.snd.transition_event_fr import TransitionEventFr


class TestTransitionEventFr(unittest.TestCase):
    """Testing TransitionEvent definitions for FR."""

    def test_missing_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key in TransitionEvent:

            if key not in TransitionEventFr:
                result.append(key.name)

        self.assertEqual(0, len(result), result)

    def test_extra_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key in TransitionEventFr:

            if key not in TransitionEvent:
                result.append(key.name)

        self.assertEqual(0, len(result), result)

    def test_empty_keys(self):

        result: list[str] = []

        # Check if all keys are present in localized version.
        for key, value in TransitionEventFr.items():

            if 1 == len(value):
                result.append(key.name)

        self.assertEqual(0, len(result), result)
