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

"""Tests for signal_point."""

import unittest
from unittest.mock import patch

import biz.dfch.scnfmixr.public.mixer.signal_point as pt

from biz.dfch.scnfmixr.mixer.signal_point import (
    BestAlsaJackAudioDevice,
    AlsaJackAudioPointManager,
)
from biz.dfch.scnfmixr.public.audio import (
    AlsaInterfaceInfo,
    Format,
    SampleRate,
)
from tests.scnfmixr.alsa_usb.mock_alsa_to_jack_base import (
    MockAlsaToJack,
    MockJackToAlsa
)

from ..alsa_usb.mock_alsa_stream_info_parser import MockAlsaStreamInfoParser


class TestBestAlsaJackAudioDevice(unittest.TestCase):
    """Testing signal_point."""

    def test_initialise_with_negative_card_id_throws(self):
        """Testing an invalid card id."""

        with self.assertRaises(AssertionError):
            _ = BestAlsaJackAudioDevice("ABC", -1)

    def test_initialise_with_invalid_card_id_throws(self):
        """Testing an invalid card id."""

        with self.assertRaises(FileNotFoundError):
            _ = BestAlsaJackAudioDevice("ABC", 5)

    def test_initialise_with_invalid_device_id_throws(self):
        """Testing an invalid device id."""

        with self.assertRaises(AssertionError):
            _ = BestAlsaJackAudioDevice("ABC", 2, 1)

    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.AlsaToJack",
           new=MockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.JackToAlsa",
           new=MockJackToAlsa)
    def test_with_valid_card_id_succeeds(self):
        """Testing something."""

        display_name = "ABC"
        card_id = 2
        parser = MockAlsaStreamInfoParser(card_id)

        sut = BestAlsaJackAudioDevice(display_name, card_id, parser=parser)

        expected = f"hw:CARD={card_id},DEV=0"

        self.assertIsNotNone(sut)

        result = sut.name

        self.assertEqual(expected, result)

    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.AlsaToJack",
           new=MockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.JackToAlsa",
           new=MockJackToAlsa)
    def test_properties(self):
        "Testing properties"

        parser = MockAlsaStreamInfoParser(2)

        sut = BestAlsaJackAudioDevice("ABC", 2, parser=parser)

        self.assertEqual(2, sut.card_id)
        self.assertEqual(0, sut.device_id)

        self.assertEqual(3, len(sut.points))

        self.assertEqual(1, len(sut.sources))
        self.assertEqual(2, len(sut.sinks))

    class MySinkPoint(pt.ISinkPoint):
        """Arbitrary sink point."""

        @property
        def is_active(self):
            raise NotImplementedError

        def connect_to(self, other):
            raise NotImplementedError

    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.AlsaToJack",
           new=MockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.JackToAlsa",
           new=MockJackToAlsa)
    def test_connect_to(self):
        """Testing connecto_to."""

        parser = MockAlsaStreamInfoParser(2)

        sut = BestAlsaJackAudioDevice("ABC", 2, parser=parser)

        sink_pt = TestBestAlsaJackAudioDevice.MySinkPoint("XYZ")

        _ = sut.connect_to(sink_pt)


class TestAlsaJackAudioPointController(unittest.TestCase):
    """Testing signal_point."""

    class MyMockAlsaToJack(MockAlsaToJack):
        """Mock with specific stop()"""

        result: list[str] = []

        def stop(self):
            self.result.append("invoked")
            return super().stop()

    class MyMockJackToAlsa(MockJackToAlsa):
        """Mock with specific stop()"""

        result: list[str] = []

        def stop(self):
            self.result.append("invoked")
            return super().stop()

    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.AlsaToJack",
           new=MyMockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.alsa_jack_audio_point.JackToAlsa",
           new=MyMockJackToAlsa)
    def test_with_resouce_manager(self):
        """Testing with resource manager releases resources."""

        card_id = 2
        parser = MockAlsaStreamInfoParser(2)

        interface = parser.get_best_capture_interface()
        source = AlsaInterfaceInfo(
            card_id=card_id,
            interface_id=parser.interface_id,
            channel_count=interface.channel_count,
            format=Format(interface.format),
            bit_depth=Format(interface.format).get_bit_depth(),
            sample_rate=SampleRate(interface.get_best_rate()),
        )
        interface = parser.get_best_playback_interface()
        sink = AlsaInterfaceInfo(
            card_id=card_id,
            interface_id=parser.interface_id,
            channel_count=interface.channel_count,
            format=Format(interface.format),
            bit_depth=Format(interface.format).get_bit_depth(),
            sample_rate=SampleRate(interface.get_best_rate()),
        )

        with AlsaJackAudioPointManager("ABC", source, sink) as sut:

            sources, sinks = sut

            self.assertEqual(1, len(sources))
            self.assertEqual(2, len(sinks))

        self.assertEqual(
            1,
            len(TestAlsaJackAudioPointController.MyMockAlsaToJack.result))
        self.assertEqual(
            1,
            len(TestAlsaJackAudioPointController.MyMockAlsaToJack.result))
