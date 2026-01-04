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

    def setUp(self):
        self._alsa_stream_info = AlsaStreamInfoVisitor()
        self._dic = {
            "Playback:": self._alsa_stream_info.process_playback,
            "Capture:": self._alsa_stream_info.process_capture,
            "Interface ": self._alsa_stream_info.process_interface,
            "Format:": self._alsa_stream_info.process_format,
            "Channels:": self._alsa_stream_info.process_channels,
            "Rates:": self._alsa_stream_info.process_rates,
            "Bits:": self._alsa_stream_info.process_bits,
            "Channel map:": self._alsa_stream_info.process_map,
        }
        return super().setUp()

    def test_parsing_stream_data_atomos_returns_single_capture_interface(self):
        """Atomos has a 'continuous' interface rate."""

        # Arrange
        alsa_stream_info = self._alsa_stream_info
        dic = self._dic

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
        alsa_stream_info = self._alsa_stream_info
        dic = self._dic

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

        alsa_stream_info = self._alsa_stream_info
        dic = self._dic

        parser = MultiLineTextParser(indent=" ",
                                     length=2,
                                     dic=dic,
                                     default=process_default)

        # Act
        parser.parse(UgreenKtMicro)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 1)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
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
            for interface in alsa_stream_info.get_interfaces()
            if interface.state == AlsaStreamInfoVisitorState.CAPTURE
            and (interface.bit_depth in (16, 24))
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[
            0].to_dict()
        log.info("best_capture: '%s'", best_capture)

    def test_parsing_stream_data_sound_devices_succeeds(self):
        """Sound Devices MixPre-6 II."""

        # Arrange
        alsa_stream_info = self._alsa_stream_info
        dic = self._dic

        parser = MultiLineTextParser(" ", 2, dic)

        # Act
        parser.parse(MixPre6II)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 2)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
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
            for interface in alsa_stream_info.get_interfaces()
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
