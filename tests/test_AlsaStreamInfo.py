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

from typing import Callable
import unittest

from src.AlsaStreamInfoState import AlsaStreamInfoState
from src.AlsaStreamInfo import AlsaStreamInfo
from src.MultiLineTextParser import MultiLineTextParser
from src.MultiLineTextParserContext import MultiLineTextParserContext
from src.log import log


class AlsaStreamInfoTest(unittest.TestCase):

    def test_parsing_stream_data_atomos_continuous_returns_single_capture_interface(self):

        # Arrange
        text = """\
MacroSilicon MS2109 at usb-xhci-hcd.0-1.2, high speed : USB Audio

Capture:
  Status: Stop
  Interface 3
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 48000 - 48000 (continuous)
    Data packet interval: 1000 us
    Bits: 0
""".splitlines()

        alsa_stream_info = AlsaStreamInfo()
        map = {
            "Playback:": alsa_stream_info.process_playback,
            "Capture:": alsa_stream_info.process_capture,
            "Interface ": alsa_stream_info.process_interface,
            "Format:": alsa_stream_info.process_format,
            "Channels:": alsa_stream_info.process_channels,
            "Rates:": alsa_stream_info.process_rates,
            "Bits:": alsa_stream_info.process_bits,
            "Channel map:": alsa_stream_info.process_map,
        }

        parser = MultiLineTextParser(text, map)

        # Act
        parser.Parse(text)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 0)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 1)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
            if interface.state == AlsaStreamInfoState.CAPTURE
            and interface.bit_depth == 0
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[0].to_dict()
        log.info(f"best_capture: {best_capture}")

    def test_parsing_stream_data_atomos_continuous_returns_no_best_interface(self):

        # Arrange
        text = """\
MacroSilicon MS2109 at usb-xhci-hcd.0-1.2, high speed : USB Audio

Capture:
  Status: Stop
  Interface 3
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 48000 - 48000 (continuous)
    Data packet interval: 1000 us
    Bits: 0
""".splitlines()

        alsa_stream_info = AlsaStreamInfo()
        map = {
            "Playback:": alsa_stream_info.process_playback,
            "Capture:": alsa_stream_info.process_capture,
            "Interface ": alsa_stream_info.process_interface,
            "Format:": alsa_stream_info.process_format,
            "Channels:": alsa_stream_info.process_channels,
            "Rates:": alsa_stream_info.process_rates,
            "Bits:": alsa_stream_info.process_bits,
            "Channel map:": alsa_stream_info.process_map,
        }

        parser = MultiLineTextParser(text, map)

        # Act
        parser.Parse(text)

        # Assert
        self.assertEqual(len(alsa_stream_info.get_playback_interfaces()), 0)
        self.assertEqual(len(alsa_stream_info.get_capture_interfaces()), 1)

        for interface in alsa_stream_info.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_info.get_interfaces()
            if interface.state == AlsaStreamInfoState.CAPTURE
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        self.assertEqual(filtered, [])

    def test_parsing_stream_data_ugreen_ktmicro_succeeds(self):

        # Arrange
        text = """\
KTMicro KT USB Audio at usb-xhci-hcd.0-1.1, full speed : USB Audio

Playback:
  Status: Stop
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ADAPTIVE)
    Rates: 44100, 48000, 96000
    Bits: 16
    Channel map: FL FR
  Interface 2
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ADAPTIVE)
    Rates: 44100, 48000, 96000
    Bits: 24
    Channel map: FL FR

Capture:
  Status: Stop
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 0x81 (1 IN) (ASYNC)
    Rates: 44100, 48000
    Bits: 16
    Channel map: MONO
""".splitlines()

        default: Callable[[MultiLineTextParserContext], None] = lambda ctx: log.debug(
            f"[#{ctx.line}][{ctx.level_previous}>{ctx.level}] default: {ctx.text}"
        )

        alsa_stream_parser = AlsaStreamInfo()
        map = {
            "Playback:": alsa_stream_parser.process_playback,
            "Capture:": alsa_stream_parser.process_capture,
            "Interface ": alsa_stream_parser.process_interface,
            "Format:": alsa_stream_parser.process_format,
            "Channels:": alsa_stream_parser.process_channels,
            "Rates:": alsa_stream_parser.process_rates,
            "Bits:": alsa_stream_parser.process_bits,
            "Channel map:": alsa_stream_parser.process_map,
        }

        parser = MultiLineTextParser(text, map, default)

        # Act
        parser.Parse(text)

        # Assert
        self.assertEqual(len(alsa_stream_parser.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_parser.get_capture_interfaces()), 1)

        for interface in alsa_stream_parser.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoState.PLAYBACK
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        best_playback = sorted(filtered, key=lambda interface: interface.format)[0].to_dict()
        log.info(f"best_playback: {best_playback}")

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoState.CAPTURE
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[0].to_dict()
        log.info(f"best_capture: {best_capture}")

    def test_parsing_stream_data_sound_devices_succeeds(self):

        # Arrange
        text = """\
Sound Devices, LLC MixPre-6 II at usb-xhci-hcd.0-2, high speed : USB Audio

Playback:
  Status: Running
    Interface = 1
    Altset = 2
    Packet Size = 432
    Momentary freq = 48002 Hz (0x6.0010)
    Feedback Format = 7.17
  Interface 1
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 16
    Channel map: FL FR
    Sync Endpoint: 0x81 (1 IN)
    Sync EP Interface: 1
    Sync EP Altset: 1
    Implicit Feedback Mode: No
  Interface 1
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 24
    Channel map: FL FR
    Sync Endpoint: 0x81 (1 IN)
    Sync EP Interface: 1
    Sync EP Altset: 2
    Implicit Feedback Mode: No

Capture:
  Status: Running
    Interface = 2
    Altset = 2
    Packet Size = 432
    Momentary freq = 48000 Hz (0x6.0000)
  Interface 2
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 16
    Channel map: FL FR
  Interface 2
    Altset 2
    Format: S24_3LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 44100, 48000, 96000
    Data packet interval: 1000 us
    Bits: 24
    Channel map: FL FR
""".splitlines()

        alsa_stream_parser = AlsaStreamInfo()
        map = {
            "Playback:": alsa_stream_parser.process_playback,
            "Capture:": alsa_stream_parser.process_capture,
            "Interface ": alsa_stream_parser.process_interface,
            "Format:": alsa_stream_parser.process_format,
            "Channels:": alsa_stream_parser.process_channels,
            "Rates:": alsa_stream_parser.process_rates,
            "Bits:": alsa_stream_parser.process_bits,
            "Channel map:": alsa_stream_parser.process_map,
        }

        parser = MultiLineTextParser(text, map)

        # Act
        parser.Parse(text)

        # Assert
        self.assertEqual(len(alsa_stream_parser.get_playback_interfaces()), 2)
        self.assertEqual(len(alsa_stream_parser.get_capture_interfaces()), 2)

        for interface in alsa_stream_parser.get_interfaces():
            log.info(interface.to_dict())

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoState.PLAYBACK
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        best_playback = sorted(filtered, key=lambda interface: interface.format)[0].to_dict()
        log.info(f"best_playback: {best_playback}")

        filtered = [
            interface
            for interface in alsa_stream_parser.get_interfaces()
            if interface.state == AlsaStreamInfoState.CAPTURE
            and (interface.bit_depth == 16 or interface.bit_depth == 24)
            and 48000 in interface.rates
        ]
        best_capture = sorted(filtered, key=lambda interface: interface.format)[0].to_dict()
        log.info(f"best_capture: {best_capture}")


if __name__ == "__main__":
    unittest.main()
