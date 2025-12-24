# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""Test for application_context."""

import unittest
from biz.dfch.scnfmixr.application_context import ApplicationContext
from biz.dfch.scnfmixr.audio import RecordingParameters


class TestApplicationContext(unittest.TestCase):
    """Test the ApplicationContext."""

    def test_singleton_identity_succeeds(self):
        """Ensure that ApplicationContext returns the same instance every
        time."""

        sut1 = ApplicationContext.Factory.get()
        sut2 = ApplicationContext.Factory.get()
        self.assertIs(sut1, sut2,
                      "ApplicationContext is not a singleton")

    def test_recording_parameters_initialised_succeeds(self):
        """Ensure that recording_parameters is initialised and is an instance
        of RecordingParameters."""

        sut = ApplicationContext.Factory.get()
        self.assertIsNotNone(sut.recording_parameters)
        self.assertIsInstance(sut.recording_parameters, RecordingParameters)

    def test_direct_instantiation_throws(self):
        """Ensure that directly calling the constructor raises RuntimeError."""

        with self.assertRaises(RuntimeError):
            # Attempting to instantiate directly without acquiring the lock
            ApplicationContext()

    def test_str_representation_contains_keys_succeeds(self):
        """Ensure that __str__ returns a string with expected keys."""

        sut = ApplicationContext.Factory.get()

        result = str(sut)

        self.assertIn("audio_map", result)
        self.assertIn("rec", result)
        self.assertIn("dat", result)


if __name__ == "__main__":
    unittest.main()
