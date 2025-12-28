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

"""Tests for signal_point."""

import unittest
from unittest.mock import patch

import biz.dfch.scnfmixr.public.mixer.iconnectable_sink_point as pt

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

    class MySinkPoint(pt.IConnectableSinkPoint):
        """Arbitrary sink point."""

        @property
        def is_active(self):
            raise NotImplementedError

        def connect_to(self, other):
            raise NotImplementedError

        def acquire(self):
            raise NotImplementedError

        def release(self):
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
