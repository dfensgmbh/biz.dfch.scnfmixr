# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

"""Module test_device_factory.

Regression tests for GitHub issue #89: the master/mix-down bus `MX0`
(whose content is copied, as the `MST_LEFT`/`MST_RIGHT` reference
channels, into tracks 0/1 of both `MX1` and `MX2`) must be fed from the
WET channel strips (`WT0`/`WT1`/`WT2`), not from the raw DRY strips
(`DR0`/`DR1`/`DR2`), and must not receive the per-performer monitor/
foldback buses (`MX3`/`MX4`/`MX5`/`MX6`) fed back into it.

`JackBusDevice.acquire()`/`connect_to()` talk to a real JACK/ecasound
graph, so `DeviceFactory.create_mixbus_group()` is exercised here
against a lightweight fake standing in for `JackBusDevice`, recording
every `connect_to()` call instead of touching JACK.
"""

import unittest
from unittest.mock import patch

from biz.dfch.scnfmixr.mixer.device_factory import DeviceFactory
from biz.dfch.scnfmixr.public.mixer import ConnectionPolicy


class _FakePoint:
    """Records single-point `connect_to()` calls."""

    def __init__(self, owner_name, index, calls):
        self.owner_name = owner_name
        self.index = index
        self._calls = calls

    def connect_to(self, other, policy=None):
        self._calls.append(
            (
                f"{self.owner_name}[{self.index}]",
                f"{other.owner_name}[{other.index}]",
                policy,
            )
        )


class _FakePointSet:
    """Lazily hands out `_FakePoint` instances, indexed like a mapping."""

    def __init__(self, owner_name, calls):
        self._owner_name = owner_name
        self._calls = calls
        self._points = {}

    def __getitem__(self, index):
        if index not in self._points:
            point = _FakePoint(self._owner_name, index, self._calls)
            self._points[index] = point
        return self._points[index]


class _FakeSinkSet:
    """Stand-in for `JackBusDevice.as_sink_set()`."""

    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.index = "*"


class FakeJackBusDevice:
    """Minimal stand-in for `JackBusDevice`.

    Implements only the surface `DeviceFactory.create_mixbus_group()`
    exercises, and records every `connect_to()` call (both device-level,
    via `as_sink_set()`, and single-point, via `sources`/`sinks`) into
    the shared, class-level `calls` list.
    """

    calls: list[tuple[str, str, object]] = []

    def __init__(self, name, channel_count=2):
        self.name = name
        self.channel_count = channel_count
        self.sources = _FakePointSet(name, FakeJackBusDevice.calls)
        self.sinks = _FakePointSet(name, FakeJackBusDevice.calls)

    def acquire(self):
        return self

    def as_sink_set(self):
        return _FakeSinkSet(self.name)

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):
        FakeJackBusDevice.calls.append((self.name, other.owner_name, policy))
        return self


@patch(
    "biz.dfch.scnfmixr.mixer.device_factory.JackBusDevice",
    new=FakeJackBusDevice,
)
class TestDeviceFactoryCreateMixbusGroup(unittest.TestCase):
    """Testing DeviceFactory.create_mixbus_group()."""

    def setUp(self):
        FakeJackBusDevice.calls.clear()

    def _dual_sources_into(self, sink_name: str) -> set[str]:
        """Names of devices DUAL-connected into `sink_name`'s sink set."""

        return {
            source
            for source, sink, policy in FakeJackBusDevice.calls
            if sink == sink_name and policy == ConnectionPolicy.DUAL
        }

    def test_mx0_is_fed_from_wet_not_dry(self):
        """MX0 (the master/mix-down bus) is fed from WT0/WT1/WT2.

        Per issue #89, it must NOT be fed directly from the raw DR0/DR1/
        DR2 strips.
        """

        DeviceFactory.create_mixbus_group()

        sources = self._dual_sources_into("MX0")

        self.assertEqual({"WT0", "WT1", "WT2"}, sources)

    def test_mx0_does_not_receive_monitor_bus_feedback(self):
        """MX3/MX4/MX5/MX6 (personal monitor/foldback buses) must not be
        routed back into MX0 (issue #89)."""

        DeviceFactory.create_mixbus_group()

        sources = self._dual_sources_into("MX0")

        self.assertTrue(sources.isdisjoint({"MX3", "MX4", "MX5", "MX6"}))

    def test_mx1_iso_channels_still_fed_from_dry_only(self):
        """MX1's explicit per-channel iso wiring still carries only DRY
        content (unaffected by the MX0 routing fix)."""

        DeviceFactory.create_mixbus_group()

        sinks_fed_by_dry = {
            sink
            for source, sink, _ in FakeJackBusDevice.calls
            if source.startswith("DR") and sink.startswith("MX1[")
        }
        sinks_fed_by_wet = {
            sink
            for source, sink, _ in FakeJackBusDevice.calls
            if source.startswith("WT") and sink.startswith("MX1[")
        }

        self.assertEqual(6, len(sinks_fed_by_dry))
        self.assertEqual(set(), sinks_fed_by_wet)

    def test_mx2_iso_channels_still_fed_from_wet_only(self):
        """MX2's explicit per-channel iso wiring still carries only WET
        content (unaffected by the MX0 routing fix)."""

        DeviceFactory.create_mixbus_group()

        sinks_fed_by_wet = {
            sink
            for source, sink, _ in FakeJackBusDevice.calls
            if source.startswith("WT") and sink.startswith("MX2[")
        }
        sinks_fed_by_dry = {
            sink
            for source, sink, _ in FakeJackBusDevice.calls
            if source.startswith("DR") and sink.startswith("MX2[")
        }

        self.assertEqual(6, len(sinks_fed_by_wet))
        self.assertEqual(set(), sinks_fed_by_dry)

    def test_mx0_still_copied_into_mx1_and_mx2_reference_channels(self):
        """MX0 (now wet-derived) is still copied wholesale into MX1 and
        MX2's sink sets, to seed their MST_LEFT/MST_RIGHT reference
        tracks."""

        DeviceFactory.create_mixbus_group()

        mx0_dual_sinks = {
            sink
            for source, sink, policy in FakeJackBusDevice.calls
            if source == "MX0" and policy == ConnectionPolicy.DUAL
        }

        self.assertIn("MX1", mx0_dual_sinks)
        self.assertIn("MX2", mx0_dual_sinks)

    def test_returns_all_thirteen_devices(self):
        """create_mixbus_group() still returns all 13 bus/strip devices."""

        result = DeviceFactory.create_mixbus_group()

        names = {device.name for device in result}
        self.assertEqual(
            {
                "MX0",
                "MX1",
                "MX2",
                "MX3",
                "MX4",
                "MX5",
                "MX6",
                "DR0",
                "WT0",
                "DR1",
                "WT1",
                "DR2",
                "WT2",
            },
            names,
        )


if __name__ == "__main__":
    unittest.main()
