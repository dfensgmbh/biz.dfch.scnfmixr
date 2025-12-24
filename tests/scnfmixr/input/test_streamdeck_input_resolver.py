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

"""TestStreamdeckInputResolver class"""

# pylint: disable=missing-function-docstring

import unittest

from biz.dfch.scnfmixr.input.streamdeck_input_resolver import (
    StreamdeckInputResolver
)
from biz.dfch.scnfmixr.public.input.input_event_map import (
    InputEventMap
)


class TestStreamdeckInputResolver(unittest.TestCase):
    """TestStreamdeckInputResolver"""

    def test_resolve_valid_state_and_invalid_key_returns_none(self):

        sut = StreamdeckInputResolver()

        key = 29  # Invalid key.
        name = "Main"

        result = sut.invoke(name, key)

        self.assertEqual(None, result)

    def test_resolve_invalid_state_and_key_returns_none(self):

        sut = StreamdeckInputResolver()

        key = 1
        name = "invalid-state"

        result = sut.invoke(name, key)

        self.assertEqual(None, result)

    def test_resolve_valid_state_and_key_returns_valid_input_event_map(self):

        sut = StreamdeckInputResolver()

        key = 1
        name = "Main"
        expected = InputEventMap.KEY_1

        result = sut.invoke(name, key)

        self.assertEqual(expected, result)
