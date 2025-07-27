# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

import unittest
from threading import Thread
from biz.dfch.scnfmixr.public.mixer.state import (
    State,
)


class TestPathStateFlag(unittest.TestCase):
    """TestPathStateFlag"""

    def test_flag_values(self):
        """Test the flags."""

        self.assertEqual(State.Flag.INITIAL, 0x01)
        self.assertEqual(State.Flag.OK, 0x02)
        self.assertEqual(State.Flag.STALE, 0x04)
        self.assertEqual(State.Flag.REMOVED, 0x08)
        self.assertEqual(State.Flag.ACQUIRED, 0x80)

    def test_combined_flags(self):
        """Test flag combinations."""
        self.assertEqual(State.Flag.ACQUIRED_INITIAL,
                         State.Flag.ACQUIRED | State.Flag.INITIAL)
        self.assertEqual(State.Flag.ACQUIRED_OK,
                         State.Flag.ACQUIRED | State.Flag.OK)
        self.assertEqual(State.Flag.ACQUIRED_STALE,
                         State.Flag.ACQUIRED | State.Flag.STALE)
        self.assertEqual(State.Flag.ACQUIRED_REMOVE,
                         State.Flag.ACQUIRED | State.Flag.REMOVED)


class TestPathState(unittest.TestCase):
    """TestPathState"""

    def test_initial_value(self):
        """Test initial value."""

        sut = State()

        self.assertEqual(sut.value, State.Flag.INITIAL)
        self.assertFalse(sut.is_acquired)

    def test_is_acquired_set_and_clear(self):
        """Acquired"""

        sut = State()

        sut.is_acquired = True
        self.assertTrue(sut.is_acquired)
        self.assertTrue(sut.value & State.Flag.ACQUIRED)

        sut.is_acquired = False
        self.assertFalse(sut.is_acquired)
        self.assertFalse(sut.value & State.Flag.ACQUIRED)

    def test_value_setter_preserves_acquired_flag(self):
        """Setter preserves acquired."""

        sut = State()

        # Set acquired first
        sut.is_acquired = True
        sut.value = State.Flag.OK
        self.assertTrue(sut.is_acquired)
        self.assertEqual(sut.value & ~
                         State.Flag.ACQUIRED, State.Flag.OK)

        # Clear acquired, change value
        sut.is_acquired = False
        sut.value = State.Flag.REMOVED
        self.assertFalse(sut.is_acquired)
        self.assertEqual(sut.value, State.Flag.REMOVED)

    def test_value_setter_invalid_type(self):
        """Invalid detection."""
        sut = State()

        with self.assertRaises(AssertionError):
            sut.value = 123  # Not a PathStateFlag

    def test_set_flag_preserves_acquired_flag(self):
        """Setter preserves acquired."""

        sut = State()

        # Set acquired first
        sut.is_acquired = True
        sut.value = State.Flag.OK
        self.assertTrue(sut.is_acquired)
        self.assertEqual(sut.value & ~
                         State.Flag.ACQUIRED, State.Flag.OK)

        # Clear acquired, change value
        sut.is_acquired = False
        sut.value = State.Flag.REMOVED
        self.assertFalse(sut.is_acquired)
        self.assertEqual(sut.value, State.Flag.REMOVED)

    def test_set_flag_invalid_type(self):
        """Invalid detection."""

        sut = State()

        with self.assertRaises(AssertionError):
            sut.value = 123  # Not a PathStateFlag

    def test_is_acquired_setter_invalid_type(self):

        sut = State()

        with self.assertRaises(AssertionError):
            sut.is_acquired = "yes"  # Not a bool

    def test_has_flag(self):

        sut = State()

        sut.value = State.Flag.OK
        self.assertTrue(sut.has_flag(State.Flag.OK))
        self.assertFalse(sut.has_flag(State.Flag.STALE))

        sut.is_acquired = True
        self.assertTrue(sut.has_flag(State.Flag.ACQUIRED))

    def test_has_flag_invalid_type(self):

        sut = State()

        with self.assertRaises(AssertionError):
            sut.has_flag(42)  # Not a PathStateFlag

    def test_str_and_repr(self):

        sut = State()

        sut.value = State.Flag.OK
        self.assertEqual(str(sut), "OK")
        self.assertEqual(repr(sut), "OK")

        # Test unknown value (non-standard flag)
        sut._value = State.Flag(0x10)  # A flag not in enum
        self.assertTrue(str(sut).startswith("0x"))

    def test_thread_safety(self):

        sut = State()

        # Basic test to ensure no exceptions on concurrent access
        def toggle_acquired():
            for _ in range(1000):
                sut.is_acquired = True
                sut.is_acquired = False

        threads = [Thread(target=toggle_acquired) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Final state is indeterminate but should be a valid PathStateFlag
        self.assertIsInstance(sut.value, State.Flag)

    def test_set_flag_preserves_acquired(self):

        sut = State()
        sut.value = State.Flag.OK
        sut.is_acquired = True

        sut.set_flag(State.Flag.STALE)
        self.assertTrue(sut.has_flag(State.Flag.STALE))
        self.assertTrue(sut.has_flag(State.Flag.ACQUIRED))
        self.assertFalse(sut.has_flag(State.Flag.OK))

    def test_set_flag_clears_old_state(self):

        sut = State()

        sut.value = State.Flag.OK
        sut.set_flag(State.Flag.REMOVED)
        self.assertTrue(sut.has_flag(State.Flag.REMOVED))
        self.assertFalse(sut.has_flag(State.Flag.OK))

    def test_set_flag_acquired_unchanged_when_unset(self):

        sut = State()

        sut.value = State.Flag.STALE
        sut.set_flag(State.Flag.INITIAL)
        self.assertEqual(sut.value, State.Flag.INITIAL)

    def test_set_flag_with_invalid_flag_raises(self):

        sut = State()

        with self.assertRaises(AssertionError):
            # This simulates passing an unsupported combination
            sut.set_flag(State.Flag.ACQUIRED)


if __name__ == "__main__":
    unittest.main()
