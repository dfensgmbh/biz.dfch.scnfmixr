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
        True: The audio will be played continuously in a loop.
        False: The audio will be play once (one-shot).
        """

        EVENT = False

    class TransitionInfoLeave(Enum):
        """Test events.
        True: The audio will be played continuously in a loop.
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

    def test_initializing_succeeds(self):
        """Initializing succeeds."""

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

    def test_initializing_target_state_none_throws(self):
        """`target_state` must not be `None`."""

        with self.assertRaises(AssertionError):
            _ = TestTransitionBase.ArbitraryTransition(
                event="0",
                info_enter=None,
                info_leave=None,
                target_state=None
            )

    def test_initializing_event_containing_multiple_characters_throws(self):
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

    def test_initializing_empty_event_throws(self):
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
