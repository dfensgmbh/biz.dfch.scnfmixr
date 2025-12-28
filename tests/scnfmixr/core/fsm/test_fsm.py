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

"""Tests for module: `Fsm`."""

import unittest

from biz.dfch.scnfmixr.core.fsm import ExecutionContext
from biz.dfch.scnfmixr.core.fsm import Fsm
from biz.dfch.scnfmixr.core.fsm import StateBase
from biz.dfch.scnfmixr.core.fsm import TransitionBase
from biz.dfch.scnfmixr.core.fsm import UserInteractionBase


class TestFsm(unittest.TestCase):
    """Tests a finite state machine."""

    class ArbitraryUserInteractionBase(UserInteractionBase):
        """Arbtirary implementation."""

        def update(self, item):
            return

    class ArbitraryState1(StateBase):
        """Defines an arbitrary state for testing purposes."""

    class ArbitraryState2(StateBase):
        """Defines an arbitrary state for testing purposes."""

    class ArbitraryTransition1(TransitionBase):
        """Defines an arbitrary transition for testing purposes."""

        def invoke(self, ctx: ExecutionContext) -> bool:

            assert ctx is not None
            assert isinstance(ctx, ExecutionContext)

            return True

    class ArbitraryTransition2(TransitionBase):
        """Defines an arbitrary transition for testing purposes."""

        def invoke(self, ctx: ExecutionContext) -> bool:

            assert ctx is not None
            assert isinstance(ctx, ExecutionContext)

            return True

    def test_initialising_succeeds(self):
        """Initializing succeeds."""

        initial_state = TestFsm.ArbitraryState1(
            info_enter=None,
            info_leave=None)
        ctx = ExecutionContext(None, None)
        ui = TestFsm.ArbitraryUserInteractionBase()

        sut = Fsm(initial_state, ctx, ui)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut.current_state, StateBase)

    def test_transiting_between_states_succeeds(self):
        """Invoking a transition between states suceeds for valid events."""

        initial_state = TestFsm.ArbitraryState1(
            info_enter=None,
            info_leave=None)

        end_state = TestFsm.ArbitraryState2(
            info_enter=None,
            info_leave=None)

        transition_to_end_state = TestFsm.ArbitraryTransition1(
            event="0",
            info_enter=None,
            info_leave=None,
            target_state=end_state
        )

        transition_to_initial_state = TestFsm.ArbitraryTransition2(
            event="1",
            info_enter=None,
            info_leave=None,
            target_state=initial_state
        )

        initial_state.add_transition(transition_to_end_state)
        end_state.add_transition(transition_to_initial_state)
        ctx = ExecutionContext(None, None)
        ui = TestFsm.ArbitraryUserInteractionBase()

        sut = Fsm(initial_state, ctx, ui)
        self.assertIsNotNone(sut)
        self.assertEqual(TestFsm.ArbitraryState1, type(sut.current_state))

        # Valid event, but will fail, as fsm is not started
        result = sut.invoke("0")
        self.assertFalse(result)

        # Start fsm
        result = sut.start()
        self.assertTrue(result)

        # Invalid event, will stay in same state.
        result = sut.invoke("9")
        self.assertFalse(result)
        self.assertEqual(TestFsm.ArbitraryState1, type(sut.current_state))

        # Valid event, will transition to new state
        result = sut.invoke("0")
        self.assertTrue(result)
        self.assertEqual(TestFsm.ArbitraryState2, type(sut.current_state))

        # Valid event, will transition (back) to first state
        result = sut.invoke("1")
        self.assertTrue(result)
        self.assertEqual(TestFsm.ArbitraryState1, type(sut.current_state))

        for line in sut.visualize():
            print(line)


if __name__ == "__main__":
    unittest.main()
