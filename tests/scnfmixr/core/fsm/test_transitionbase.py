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

"""Tests for module: `Transition`."""

from enum import Enum
import unittest

from biz.dfch.scnfmixr.core.fsm import UiEventInfo
from biz.dfch.scnfmixr.core.fsm import ExecutionContext
from biz.dfch.scnfmixr.core.fsm import StateBase
from biz.dfch.scnfmixr.core.fsm import TransitionBase


class TestTransitionBase(unittest.TestCase):
    """Tests transitions in a state machine."""

    class TransitionInfoEnter(Enum):
        """Test events.
        True: The audio will be played continously in a loop.
        False: The audio will be play once (one-shot).
        """

        EVENT = False

    class TransitionInfoLeave(Enum):
        """Test events.
        True: The audio will be played continously in a loop.
        False: The audio will be play once (one-shot).
        """

        EVENT = False

    class ArbitraryState(StateBase):
        """Defines an arbitrary state for testing purposes."""

    class ArbitraryTransition(TransitionBase):
        """Defines an arbitrary transition for testing purposes."""

        def invoke(self, ctx: ExecutionContext) -> bool:

            assert ctx is not None
            assert isinstance(ctx, ExecutionContext)

            return False

    def test_initialising_succeeds(self):
        """Initialising succeeds."""

        arbitrary_state = TestTransitionBase.ArbitraryState(
            info_enter=None, info_leave=None)

        sut = TestTransitionBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo(
                TestTransitionBase.TransitionInfoEnter.EVENT, False),
            info_leave=UiEventInfo(
                TestTransitionBase.TransitionInfoLeave.EVENT, False),
            target_state=arbitrary_state
        )

        assert sut is not None

    def test_initialising_target_state_none_throws(self):
        """`target_state` must not be `None`."""

        with self.assertRaises(AssertionError):
            _ = TestTransitionBase.ArbitraryTransition(
                event="0",
                info_enter=None,
                info_leave=None,
                target_state=None
            )

    def test_initialising_event_containing_multiple_characters_throws(self):
        """`event` must not contain more than a single character."""

        arbitrary_state = TestTransitionBase.ArbitraryState(
            info_enter=None, info_leave=None)

        with self.assertRaises(AssertionError):
            _ = TestTransitionBase.ArbitraryTransition(
                event="12",
                info_enter=None,
                info_leave=None,
                target_state=arbitrary_state
            )

    def test_initialising_empty_event_throws(self):
        """`event` must not contain more than a single character."""

        arbitrary_state = TestTransitionBase.ArbitraryState(
            info_enter=None, info_leave=None)

        with self.assertRaises(AssertionError):
            _ = TestTransitionBase.ArbitraryTransition(
                event="",
                info_enter=None,
                info_leave=None,
                target_state=arbitrary_state
            )

    def test_invoke_with_ctx_none_throws(self):
        """Passing `None` or wrong data type as context to `invoke` throws."""

        arbitrary_state = TestTransitionBase.ArbitraryState(
            info_enter=None, info_leave=None)

        sut = TestTransitionBase.ArbitraryTransition(
            event="0",
            info_enter=UiEventInfo("arbitrary-start", False),
            info_leave=UiEventInfo("arbitrary-end", False),
            target_state=arbitrary_state
        )

        assert sut is not None

        with self.assertRaises(AssertionError):
            sut.invoke(ctx=None)

        with self.assertRaises(AssertionError):
            sut.invoke(ctx="wrong-data-type")


if __name__ == "__main__":
    unittest.main()
