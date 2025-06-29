# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests for module: `Fsm`."""

import unittest

from ui import ExecutionContext, Fsm
from ui import StateBase
from ui import TransitionBase


class TestFsm(unittest.TestCase):
    """Tests a finite state machine."""

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
        """Initialising succeeds."""

        initial_state = TestFsm.ArbitraryState1(info_start=None, info_end=None)
        ctx = ExecutionContext()

        sut = Fsm(initial_state, ctx)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut.current_state, StateBase)

    def test_transiting_between_states_succeeds(self):
        """Invoking a transition between states suceeds for valid events."""

        initial_state = TestFsm.ArbitraryState1(info_start=None, info_end=None)

        end_state = TestFsm.ArbitraryState2(info_start=None, info_end=None)

        transition_to_end_state = TestFsm.ArbitraryTransition1(
            event="0",
            info_start=None,
            do_info_start_loop=True,
            info_end=None,
            do_info_end_loop=True,
            target_state=end_state
        )

        transition_to_initial_state = TestFsm.ArbitraryTransition2(
            event="1",
            info_start=None,
            do_info_start_loop=True,
            info_end=None,
            do_info_end_loop=True,
            target_state=initial_state
        )

        initial_state.add_transition(transition_to_end_state)
        end_state.add_transition(transition_to_initial_state)
        ctx = ExecutionContext()

        sut = Fsm(initial_state, ctx)
        self.assertIsNotNone(sut)
        self.assertEqual(TestFsm.ArbitraryState1, type(sut.current_state))

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

        for line in sut.visualise():
            print(line)


if __name__ == "__main__":
    unittest.main()
