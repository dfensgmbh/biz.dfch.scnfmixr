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
from biz.dfch.scnfmixr.application_context import ApplicationContext
from biz.dfch.scnfmixr.audio import RecordingParameters


class TestApplicationContext(unittest.TestCase):
    """Test the ApplicationContext."""

    def test_singleton_identity(self):
        """Ensure that ApplicationContext returns the same instance every
        time."""

        instance1 = ApplicationContext.Factory.get()
        instance2 = ApplicationContext.Factory.get()
        self.assertIs(instance1, instance2,
                      "ApplicationContext is not a singleton")

    def test_recording_parameters_initialized(self):
        """Ensure that recording_parameters is initialized and is an instance
        of RecordingParameters."""

        app_ctx = ApplicationContext.Factory.get()
        self.assertIsNotNone(app_ctx.recording_parameters,
                             "recording_parameters is None")
        self.assertIsInstance(
            app_ctx.recording_parameters,
            RecordingParameters,
            "recording_parameters is not of type RecordingParameters")

    def test_no_direct_instantiation(self):
        """Ensure that directly calling the constructor raises RuntimeError."""

        with self.assertRaises(RuntimeError):
            # Attempting to instantiate directly without acquiring the lock
            ApplicationContext()

    def test_str_representation_contains_keys(self):
        """Ensure that __str__ returns a string with expected keys."""

        app_ctx = ApplicationContext.Factory.get()

        s = str(app_ctx)
        self.assertIn("audio_map", s)
        self.assertIn("rec", s)
        self.assertIn("dat", s)


if __name__ == "__main__":
    unittest.main()
