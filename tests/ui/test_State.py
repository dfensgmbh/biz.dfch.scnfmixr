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

"""Tests for module: `State`."""

import unittest

from ui import StateBase
from ui import TransitionBase, ExecutionContext


class TestState(unittest.TestCase):
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

        arbitrary_state = TestState.ArbitraryState(
            info_start=None, info_end=None)

        sut = TestState.ArbitraryTransition(
            event="0",
            info_start="arbitrary-start",
            do_info_start_loop=True,
            info_end="arbitrary-end",
            do_info_end_loop=True,
            target_state=arbitrary_state
        )

        assert sut is not None

    def test_initialising_target_state_none_throws(self):
        """`target_state` must not be `None`."""

        with self.assertRaises(AssertionError):
            _ = TestState.ArbitraryTransition(
                event="0",
                info_start=None,
                do_info_start_loop=True,
                info_end=None,
                do_info_end_loop=True,
                target_state=None
            )

    def test_initialising_event_containing_multiple_characters_throws(self):
        """`event` must not contain more than a single character."""

        arbitrary_state = TestState.ArbitraryState(
            info_start=None, info_end=None)

        with self.assertRaises(AssertionError):
            _ = TestState.ArbitraryTransition(
                event="12",
                info_start=None,
                do_info_start_loop=True,
                info_end=None,
                do_info_end_loop=True,
                target_state=arbitrary_state
            )

    def test_adding_transition_succeeds(self):
        """Adding a valid transition to a State adds it to the list of
        transitions."""

        arbitrary_state = TestState.ArbitraryState(
            info_start=None, info_end=None)

        transition = TestState.ArbitraryTransition(
            event="0",
            info_start="arbitrary-start",
            do_info_start_loop=True,
            info_end="arbitrary-end",
            do_info_end_loop=True,
            target_state=arbitrary_state
        )

        sut = TestState.ArbitraryState(info_start=None, info_end=None)

        self.assertEqual(0, len(sut.transitions))
        sut.add_transition(transition)
        self.assertEqual(1, len(sut.transitions))

    def test_adding_transition_twice_throws(self):
        """Adding the same transition twice fails."""

        arbitrary_state = TestState.ArbitraryState(
            info_start=None, info_end=None)

        transition = TestState.ArbitraryTransition(
            event="0",
            info_start="arbitrary-start",
            do_info_start_loop=True,
            info_end="arbitrary-end",
            do_info_end_loop=True,
            target_state=arbitrary_state
        )

        sut = TestState.ArbitraryState(info_start=None, info_end=None)
        sut.add_transition(transition)

        with self.assertRaises(AssertionError):
            sut.add_transition(transition)

    def test_adding_duplicate_transition_name_throws(self):
        """Adding the same transition name twice fails."""

        arbitrary_state = TestState.ArbitraryState(
            info_start=None, info_end=None)

        transition1 = TestState.ArbitraryTransition(
            event="0",
            info_start="arbitrary-start",
            do_info_start_loop=True,
            info_end="arbitrary-end",
            do_info_end_loop=True,
            target_state=arbitrary_state
        )

        transition2 = TestState.ArbitraryTransition(
            event="0",
            info_start="arbitrary-start",
            do_info_start_loop=True,
            info_end="arbitrary-end",
            do_info_end_loop=True,
            target_state=arbitrary_state
        )

        sut = TestState.ArbitraryState(info_start=None, info_end=None)
        sut.add_transition(transition1)

        with self.assertRaises(AssertionError):
            sut.add_transition(transition2)


if __name__ == "__main__":
    unittest.main()
