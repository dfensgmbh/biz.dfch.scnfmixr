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

"""Tests for module: `State`."""

import unittest

from biz.dfch.scnfmixr.core.fsm import UiEventInfo
from biz.dfch.scnfmixr.core.fsm import ExecutionContext
from biz.dfch.scnfmixr.core.fsm import StateBase
from biz.dfch.scnfmixr.core.fsm import TransitionBase


class TestStateBase(unittest.TestCase):
    """Tests states in a state machine."""

    class ArbitraryState(StateBase):
        """Defines an arbitrary state for testing purposes."""

    class ArbitraryTransition(TransitionBase):
        """Defines an arbitrary transition for testing purposes."""

        def invoke(self, ctx: ExecutionContext) -> bool:

            assert ctx is not None
            assert isinstance(ctx, ExecutionContext)

            return False
        invoke.__doc__ = TransitionBase.invoke.__doc__

    def test_initialising_succeeds(self):
        """Initialising succeeds."""

        arbitrary_state = TestStateBase.ArbitraryState(
            info_enter=None, info_leave=None)

        sut = TestStateBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        assert sut is not None

    def test_initialising_target_state_none_throws(self):
        """`target_state` must not be `None`."""

        with self.assertRaises(AssertionError):
            _ = TestStateBase.ArbitraryTransition(
                event="0",
                info_enter=None,
                info_leave=None,
                target_state=None
            )

    def test_initialising_event_containing_multiple_characters_throws(self):
        """`event` must not contain more than a single character."""

        arbitrary_state = TestStateBase.ArbitraryState(
            info_enter=None, info_leave=None)

        with self.assertRaises(AssertionError):
            _ = TestStateBase.ArbitraryTransition(
                event="12",
                info_enter=None,
                info_leave=None,
                target_state=arbitrary_state
            )

    def test_adding_transition_succeeds(self):
        """Adding a valid transition to a State adds it to the list of
        transitions."""

        arbitrary_state = TestStateBase.ArbitraryState(
            info_enter=None, info_leave=None)

        transition = TestStateBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        sut = TestStateBase.ArbitraryState(info_enter=None, info_leave=None)

        self.assertEqual(0, len(sut.transitions))
        sut.add_transition(transition)
        self.assertEqual(1, len(sut.transitions))

    def test_adding_transition_twice_throws(self):
        """Adding the same transition twice fails."""

        arbitrary_state = TestStateBase.ArbitraryState(
            info_enter=None, info_leave=None)

        transition = TestStateBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        sut = TestStateBase.ArbitraryState(info_enter=None, info_leave=None)
        sut.add_transition(transition)

        with self.assertRaises(AssertionError):
            sut.add_transition(transition)

    def test_adding_duplicate_transition_name_throws(self):
        """Adding the same transition name twice fails."""

        arbitrary_state = TestStateBase.ArbitraryState(
            info_enter=None, info_leave=None)

        transition1 = TestStateBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        transition2 = TestStateBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        sut = TestStateBase.ArbitraryState(info_enter=None, info_leave=None)
        sut.add_transition(transition1)

        with self.assertRaises(AssertionError):
            sut.add_transition(transition2)


if __name__ == "__main__":
    unittest.main()
