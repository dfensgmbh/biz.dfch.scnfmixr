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

"""Module test_jack_alsa_device."""

import unittest
from unittest.mock import patch, MagicMock

from biz.dfch.scnfmixr.public.mixer.iterminal_source_point import ITerminalSourcePoint
from biz.dfch.scnfmixr.public.mixer.iterminal_sink_point import ITerminalSinkPoint
from text import MultiLineTextParser
from biz.dfch.logging import log
from biz.dfch.scnfmixr.mixer.jack_alsa_device import JackAlsaDevice

from biz.dfch.scnfmixr.jack_commands import JackConnection

from biz.dfch.scnfmixr.public.mixer import (
    IConnectablePoint,
    IConnectableSourcePoint,
    IConnectableSinkPoint,
)

from biz.dfch.scnfmixr.public.mixer.iconnectable_device import (
    IConnectableDevice
)
from biz.dfch.scnfmixr.public.mixer.iterminal_device import ITerminalDevice
from biz.dfch.scnfmixr.public.mixer.connection_info import ConnectionInfo

from biz.dfch.scnfmixr.public.messages import Topology

from ..jack_commands.mock_process import MockProcessGetConnections3
from ..alsa_usb.mock_alsa_stream_info_parser import MockAlsaStreamInfoParser
from ..alsa_usb.mock_alsa_to_jack_base import MockAlsaToJack, MockJackToAlsa


class MockConnectionInfo:
    """MockConnectionInfo"""

    @staticmethod
    def get() -> dict[tuple[str, bool], list[str]]:
        """Gets connnections with source and sink information.

        Returns:
            dict (tuple[str, bool], list[str])
        """

        text, _ = MockProcessGetConnections3().communicate(
            ["mock-jack-lsp"])
        visitor = JackConnection.ConnectionVisitor3()

        dic = {
            "properties: input,": visitor.process_properties_input,
            "properties: output,": visitor.process_properties_output,
        }
        parser = MultiLineTextParser(
            indent=" ",
            length=1,
            dic=dic,  # type: ignore[arg-type]
            default=visitor.process_default)
        parser.parse(text, is_regex=False)

        return visitor.result


class AConnectablePoint(IConnectablePoint):
    """AConnectablePoint"""

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    @property
    def is_source(self):
        raise NotImplementedError

    @property
    def is_sink(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_active(self):
        raise NotImplementedError

    @property
    def is_acquired(self):
        raise NotImplementedError

    @is_acquired.setter
    def is_acquired(self, value):
        raise NotImplementedError


class ATerminalSourcePoint(ITerminalSourcePoint, IConnectableSourcePoint):
    """AConnectableSourcePoint"""

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    @property
    def is_sink(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_active(self):
        raise NotImplementedError

    @property
    def is_acquired(self):
        raise NotImplementedError

    @is_acquired.setter
    def is_acquired(self, value):
        raise NotImplementedError


class ATerminalSinkPoint(ITerminalSinkPoint, IConnectableSinkPoint):
    """AConnectableSinkPoint"""

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    @property
    def is_source(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_active(self):
        raise NotImplementedError

    @property
    def is_acquired(self):
        raise NotImplementedError

    @is_acquired.setter
    def is_acquired(self, value):
        raise NotImplementedError


class MockMessageQueue(MagicMock):
    """MockMessageQueue"""

    result: list[tuple[str, str]] = []

    def publish(self, arg1, _: object = 0):
        """publish"""
        log.debug("publish '[%s]' [value: '%s'].",
                  arg1, getattr(arg1, "value", None))

        MockMessageQueue.result.append(
            (type(arg1).__name__, getattr(arg1, "value", "")))

    class Factory(MagicMock):
        """Factory"""
        @staticmethod
        def get():
            """get"""
            return MockMessageQueue()


class TestJackAlsaDevice(unittest.TestCase):
    """Testing JackAlsaDevice."""

    def test_main_characteristics(self):
        """Testing main characteristics."""

        card_id = 2
        sut = JackAlsaDevice("XYZ", card_id, 0,
                             MockAlsaStreamInfoParser(card_id))

        self.assertIsInstance(sut, IConnectableDevice)
        self.assertIsInstance(sut, ITerminalDevice)
        self.assertTrue(sut.is_sink)
        self.assertTrue(sut.is_source)
        self.assertTrue(sut.is_set)
        self.assertFalse(sut.is_point)

    def test_points_count(self):
        """Testing count items in points"""

        pt = AConnectablePoint("a-point")

        card_id = 2
        sut = JackAlsaDevice("XYZ", card_id, 0,
                             MockAlsaStreamInfoParser(card_id))

        sut.add(pt)

        self.assertEqual(1, len(sut))
        self.assertEqual(0, len(sut.sources))
        self.assertEqual(0, len(sut.sinks))

    def test_sources_count(self):
        """Testing count items in points"""

        pt = ATerminalSourcePoint("a-terminal-source-point")

        card_id = 2
        sut = JackAlsaDevice("XYZ", card_id, 0,
                             MockAlsaStreamInfoParser(card_id))

        sut.add(pt)

        self.assertEqual(1, len(sut))
        self.assertEqual(1, len(sut.sources))
        self.assertEqual(0, len(sut.sinks))

    def test_sinks_count(self):
        """Testing count items in points"""

        pt = ATerminalSinkPoint("a-terminal-sink-point")

        card_id = 2
        sut = JackAlsaDevice("XYZ", card_id, 0,
                             MockAlsaStreamInfoParser(card_id))

        sut.add(pt)

        self.assertEqual(1, len(sut))
        self.assertEqual(0, len(sut.sources))
        self.assertEqual(1, len(sut.sinks))

    def test_initialsing_with_deviceid1_throws(self):
        """Initializing with device id !=1 throws."""

        card_id = 2
        with self.assertRaises(AssertionError):
            _ = JackAlsaDevice("XYZ", card_id, 1,
                               MockAlsaStreamInfoParser(card_id))

    def test_initialsing_succeeds(self):
        """Initializing with card and stream info succeeds."""

        card_id = 2
        sut = JackAlsaDevice("XYZ", card_id, 0,
                             MockAlsaStreamInfoParser(card_id))
        self.assertEqual("Alsa:XYZ", sut.name)
        self.assertEqual(0, len(sut))
        self.assertEqual(0, len(sut.points))

    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.AlsaToJack",
           new=MockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.JackToAlsa",
           new=MockJackToAlsa)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.MessageQueue",
           new=MockMessageQueue)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.MessageQueue",
           new=MockMessageQueue)
    def test_acquire_succeeds(self):
        """test"""

        logical_name = "LCL"
        device_name = f"Alsa:{logical_name}"
        card_id = 0
        device_id = 0

        mock = MockMessageQueue.result
        mock.clear()

        sut = JackAlsaDevice(logical_name, card_id, device_id,
                             MockAlsaStreamInfoParser(card_id))
        self.assertEqual(device_name, sut.name)
        self.assertEqual(0, len(sut))
        self.assertEqual(0, len(sut.points))

        sut.acquire()
        self.assertEqual(5, len(mock), mock)
        self.assertEqual(("DeviceAddingNotification", device_name), mock[0])
        self.assertEqual(
            ("PointAddingNotification", f"{device_name}-I:capture_1"), mock[1])
        self.assertEqual(
            ("PointAddingNotification", f"{device_name}-O:playback_1"), mock[2])
        self.assertEqual(
            ("PointAddingNotification", f"{device_name}-O:playback_2"), mock[3])
        self.assertEqual(("DeviceAddedNotification", device_name), mock[4])

        mock.clear()
        values3 = MockConnectionInfo().get()
        info = ConnectionInfo(values3)
        msg = Topology.ChangedNotification(info)

        # Simulating queue notifications. Direct access ok.
        sut._on_message(msg)  # pylint: disable=W0212

        self.assertEqual(3, len(mock), mock)
        self.assertEqual(
            ("PointAddedNotification", f"{device_name}-I:capture_1"), mock[0])
        self.assertEqual(
            ("PointAddedNotification", f"{device_name}-O:playback_1"), mock[1])
        self.assertEqual(
            ("PointAddedNotification", f"{device_name}-O:playback_2"), mock[2])

        mock.clear()
        sut.release()
        self.assertEqual(8, len(mock), mock)

        self.assertEqual(("DeviceRemovingNotification", device_name), mock[0])

        self.assertEqual(
            ("PointRemovingNotification",
             f"{device_name}-I:capture_1"), mock[1])
        self.assertEqual(
            ("PointRemovedNotification",
             f"{device_name}-I:capture_1"), mock[2])
        self.assertEqual(
            ("PointRemovingNotification",
             f"{device_name}-O:playback_1"), mock[3])
        self.assertEqual(
            ("PointRemovingNotification",
             f"{device_name}-O:playback_2"), mock[4])
        self.assertEqual(
            ("PointRemovedNotification",
             f"{device_name}-O:playback_2"), mock[5])
        self.assertEqual(
            ("PointRemovedNotification",
             f"{device_name}-O:playback_1"), mock[6])

        self.assertEqual(("DeviceRemovedNotification", device_name), mock[7])

    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.AlsaToJack",
           new=MockAlsaToJack)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.JackToAlsa",
           new=MockJackToAlsa)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.MessageQueue",
           new=MockMessageQueue)
    @patch("biz.dfch.scnfmixr.mixer.jack_alsa_device.MessageQueue",
           new=MockMessageQueue)
    def test_connect_to_succeeds(self):
        """test"""

        self.skipTest(1)

        # logical_name = "LCL"
        # device_name = f"Alsa:{logical_name}"
        # card_id = 0
        # device_id = 0

        # mock = MockMessageQueue.result
        # mock.clear()

        # sut = JackAlsaDevice(logical_name, card_id, device_id,
        #                      MockAlsaStreamInfoParser(card_id))

        # sut.connect_to()
