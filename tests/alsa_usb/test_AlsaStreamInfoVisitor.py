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

from biz.dfch.logging import log

from biz.dfch.scnfmixr.alsa_usb import AlsaStreamInfoParser
from biz.dfch.scnfmixr.alsa_usb import AlsaStreamInfoVisitor
from biz.dfch.scnfmixr.alsa_usb import AlsaStreamInfoVisitorState

from text.MultiLineTextParser import MultiLineTextParser
from text.MultiLineTextParserContext import MultiLineTextParserContext

from .alsa_stream0 import MacroSiliconMS2109
from .alsa_stream0 import UgreenKtMicro
from .alsa_stream0 import MixPre6II
from .alsa_stream0 import Capture44100


class TestAlsaStreamInfoVisitor(unittest.TestCase):
    """Class for testing sound card stream info."""

    def test_parsing_stream_data_atomos_returns_single_capture_interface(self):
        """Atomos has a 'continuous' interface rate."""

        # Arrange
        alsa_stream_info = AlsaStreamInfoVisitor()
        dic = {
            "Playback:": alsa_stream_info.process_playback,
            "Capture:": alsa_stream_info.process_capture,
            "Interface ": alsa_stream_info.process_interface,
            "Format:": alsa_stream_info.process_format,
            "Channels:": alsa_stream_info.process_channels,
            "Rates:": alsa_stream_info.process_rates,
            "Bits:": alsa_stream_info.process_bits,
            "Channel map:": alsa_stream_info.process_map,
        }

        parser = MultiLineTextParser(indent=" ", length=2, dic=dic)

        # Act
        parser.parse(MacroSiliconMS2109)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 0)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 1)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.CAPTURE
            and interface.bit_depth == 0
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[
            0].to_dict()
        log.info("best_capture: '%s'", best_capture)

    def test_parsing_stream_data_atomos_returns_no_best_interface(self):
        """Atomos has a 'continuous' interface rate."""

        # Arrange
        alsa_stream_info = AlsaStreamInfoVisitor()
        dic = {
            "Playback:": alsa_stream_info.process_playback,
            "Capture:": alsa_stream_info.process_capture,
            "Interface ": alsa_stream_info.process_interface,
            "Format:": alsa_stream_info.process_format,
            "Channels:": alsa_stream_info.process_channels,
            "Rates:": alsa_stream_info.process_rates,
            "Bits:": alsa_stream_info.process_bits,
            "Channel map:": alsa_stream_info.process_map,
        }

        parser = MultiLineTextParser(indent=" ", length=2, dic=dic)

        # Act
        parser.parse(MacroSiliconMS2109)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 0)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 1)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.CAPTURE
            and (interface.bit_depth in (16, 24))
            and 48000 in interface.rates
        ]
        self.assertEqual(filtered, [])

    def test_parsing_stream_data_ugreen_ktmicro_succeeds(self):
        """Ugreen KTMicro interface card."""

        # Arrange
        def process_default(ctx: MultiLineTextParserContext) -> bool:
            log.debug("[#%s][%s>%s] default: %s",
                      ctx.line,
                      ctx.level_previous,
                      ctx.level,
                      ctx.text)

            return True

        alsa_stream_parser = AlsaStreamInfoVisitor()
        dic = {
            "Playback:": alsa_stream_parser.process_playback,
            "Capture:": alsa_stream_parser.process_capture,
            "Interface ": alsa_stream_parser.process_interface,
            "Format:": alsa_stream_parser.process_format,
            "Channels:": alsa_stream_parser.process_channels,
            "Rates:": alsa_stream_parser.process_rates,
            "Bits:": alsa_stream_parser.process_bits,
            "Channel map:": alsa_stream_parser.process_map,
        }

        parser = MultiLineTextParser(indent=" ",
                                     length=2,
                                     dic=dic,
                                     default=process_default)

        # Act
        parser.parse(UgreenKtMicro)

        # Assert
        self.assertEqual(len(alsa_stream_parser.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_parser.get_capture_interfaces()), 1)

        for interface in alsa_stream_parser.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.PLAYBACK
            and (interface.bit_depth in (16, 24))
            and 48000 in interface.rates
        ]
        best_playback = sorted(
            filtered,
            key=lambda interface: interface.format)[0].to_dict()
        log.info("best_playback: '%s'", best_playback)

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.CAPTURE
            and (interface.bit_depth in (16, 24))
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[
            0].to_dict()
        log.info("best_capture: '%s'", best_capture)

    def test_parsing_stream_data_sound_devices_succeeds(self):
        """Sound Deivces MixPre-6 II."""

        # Arrange
        alsa_stream_parser = AlsaStreamInfoVisitor()
        dic = {
            "Playback:": alsa_stream_parser.process_playback,
            "Capture:": alsa_stream_parser.process_capture,
            "Interface ": alsa_stream_parser.process_interface,
            "Format:": alsa_stream_parser.process_format,
            "Channels:": alsa_stream_parser.process_channels,
            "Rates:": alsa_stream_parser.process_rates,
            "Bits:": alsa_stream_parser.process_bits,
            "Channel map:": alsa_stream_parser.process_map,
        }

        parser = MultiLineTextParser(" ", 2, dic)

        # Act
        parser.parse(MixPre6II)

        # Assert
        self.assertEqual(len(alsa_stream_parser.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_parser.get_capture_interfaces()), 2)

        for interface in alsa_stream_parser.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.PLAYBACK
            and (interface.bit_depth in (16, 24))
            and 48000 in interface.rates
        ]
        best_playback = sorted(
            filtered,
            key=lambda interface: interface.format)[0].to_dict()
        log.info("best_playback: '%s'", best_playback)

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.CAPTURE
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[
            0].to_dict()
        log.info("best_capture: '%s'", best_capture)

    def test_parsing_stream_data_44100_only_succeeds(self):
        """USB interface with 44100Hz only."""

        # Arrange
        sut = AlsaStreamInfoParser(Capture44100)

        result = sut.get_best_capture_interface()

        self.assertIsNotNone(result)
        self.assertEqual(2, result.channel_count)
        self.assertEqual(16, result.bit_depth)
        self.assertEqual("S16_LE", result.format)

        result = sut.best_rate(result.rates)
        self.assertEqual(44100, result)


if __name__ == "__main__":
    unittest.main()
