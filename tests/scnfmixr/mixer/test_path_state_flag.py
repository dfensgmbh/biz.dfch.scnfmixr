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
from biz.dfch.scnfmixr.mixer.path_state_flag import PathStateFlag
from biz.dfch.scnfmixr.mixer.path_state import PathState


class TestPathStateFlag(unittest.TestCase):
    """TestPathStateFlag"""

    def test_flag_values(self):
        """Test the flags."""

        self.assertEqual(PathStateFlag.INITIAL, 0x01)
        self.assertEqual(PathStateFlag.OK, 0x02)
        self.assertEqual(PathStateFlag.STALE, 0x04)
        self.assertEqual(PathStateFlag.REMOVED, 0x08)
        self.assertEqual(PathStateFlag.ACQUIRED, 0x80)

    def test_combined_flags(self):
        """Test flag combinations."""
        self.assertEqual(PathStateFlag.ACQUIRED_INITIAL,
                         PathStateFlag.ACQUIRED | PathStateFlag.INITIAL)
        self.assertEqual(PathStateFlag.ACQUIRED_OK,
                         PathStateFlag.ACQUIRED | PathStateFlag.OK)
        self.assertEqual(PathStateFlag.ACQUIRED_STALE,
                         PathStateFlag.ACQUIRED | PathStateFlag.STALE)
        self.assertEqual(PathStateFlag.ACQUIRED_REMOVE,
                         PathStateFlag.ACQUIRED | PathStateFlag.REMOVED)


class TestPathState(unittest.TestCase):
    """TestPathState"""

    def setUp(self):
        self.state = PathState()

    def test_initial_value(self):
        """Test initial value."""

        self.assertEqual(self.state.value, PathStateFlag.INITIAL)
        self.assertFalse(self.state.is_acquired)

    def test_is_acquired_set_and_clear(self):
        """Acquired"""

        self.state.is_acquired = True
        self.assertTrue(self.state.is_acquired)
        self.assertTrue(self.state.value & PathStateFlag.ACQUIRED)

        self.state.is_acquired = False
        self.assertFalse(self.state.is_acquired)
        self.assertFalse(self.state.value & PathStateFlag.ACQUIRED)

    def test_value_setter_preserves_acquired_flag(self):
        """Setter preserves acquired."""
        # Set acquired first
        self.state.is_acquired = True
        self.state.value = PathStateFlag.OK
        self.assertTrue(self.state.is_acquired)
        self.assertEqual(self.state.value & ~
                         PathStateFlag.ACQUIRED, PathStateFlag.OK)

        # Clear acquired, change value
        self.state.is_acquired = False
        self.state.value = PathStateFlag.REMOVED
        self.assertFalse(self.state.is_acquired)
        self.assertEqual(self.state.value, PathStateFlag.REMOVED)

    def test_value_setter_invalid_type(self):
        """Invalid detection."""
        with self.assertRaises(AssertionError):
            self.state.value = 123  # Not a PathStateFlag

    def test_is_acquired_setter_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.state.is_acquired = "yes"  # Not a bool

    def test_has_flag(self):
        self.state.value = PathStateFlag.OK
        self.assertTrue(self.state.has_flag(PathStateFlag.OK))
        self.assertFalse(self.state.has_flag(PathStateFlag.STALE))

        self.state.is_acquired = True
        self.assertTrue(self.state.has_flag(PathStateFlag.ACQUIRED))

    def test_has_flag_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.state.has_flag(42)  # Not a PathStateFlag

    def test_str_and_repr(self):
        self.state.value = PathStateFlag.OK
        self.assertEqual(str(self.state), "OK")
        self.assertEqual(repr(self.state), "OK")

        # Test unknown value (non-standard flag)
        self.state._value = PathStateFlag(0x10)  # A flag not in enum
        self.assertTrue(str(self.state).startswith("0x"))

    def test_thread_safety(self):
        # Basic test to ensure no exceptions on concurrent access
        def toggle_acquired():
            for _ in range(1000):
                self.state.is_acquired = True
                self.state.is_acquired = False

        threads = [Thread(target=toggle_acquired) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Final state is indeterminate but should be a valid PathStateFlag
        self.assertIsInstance(self.state.value, PathStateFlag)


if __name__ == "__main__":
    unittest.main()
