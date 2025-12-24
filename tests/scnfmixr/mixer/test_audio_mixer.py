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

"""Module test_audio_mixer."""

import unittest

from biz.dfch.scnfmixr.mixer import AudioMixer
from biz.dfch.scnfmixr.mixer import AudioMixerState
from biz.dfch.scnfmixr.mixer import AudioMixerConfiguration
from biz.dfch.scnfmixr.public.mixer import Connection


class TestAudioMixer(unittest.TestCase):
    """Testing AudioMixer."""

    def test_singleton_succeeds(self):
        """Factory returns only one instance."""

        sut = AudioMixer.Factory.get()
        self.assertIsNotNone(sut)

        sut2 = AudioMixer.Factory.get()
        self.assertIsNotNone(sut2)

        self.assertIs(sut, sut2)

    def test_stop_succeeds(self):
        """AudioMixerState is STOPPED after get and thus stop returns True.

        This is a problematic test, as it depends on a state."""

        sut = AudioMixer.Factory.get()

        result = sut.stop()

        self.assertTrue(result)

    def test_start_returns_false_when_not_initialised(self):
        """start returns false when not initialised.

        This is a problematic test, as it depends on a state.
        """

        sut = AudioMixer.Factory.get()

        result = sut.start()

        self.assertFalse(result)

    def test_initialise_succeds(self):
        """Initialising succeeds."""

        sut = AudioMixer.Factory.get()

        result = sut.initialise()

        self.assertTrue(result)
