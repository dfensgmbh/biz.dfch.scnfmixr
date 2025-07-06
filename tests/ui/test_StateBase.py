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

from biz.dfch.scnfmixr.ui import UiEventInfo
from biz.dfch.scnfmixr.ui import ExecutionContext
from biz.dfch.scnfmixr.ui import StateBase
from biz.dfch.scnfmixr.ui import TransitionBase


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
