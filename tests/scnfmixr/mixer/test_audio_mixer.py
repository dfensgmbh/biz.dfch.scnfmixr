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
