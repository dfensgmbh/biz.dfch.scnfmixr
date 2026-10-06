# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

# pylint: disable=E0110

"""Module device_factory."""

from ..alsa_usb import AlsaStreamInfoParser
from ..public.mixer import (
    MixbusDevice,
    IsoChannelDry,
    IsoChannelWet,
)
from ..public.mixer import ConnectionPolicy
from .jack_alsa_device import JackAlsaDevice
from .jack_bus_device import JackBusDevice


class DeviceFactory:
    """Creates audio and mixer devices and device groups."""

    @staticmethod
    def create_jack_alsa(
        name: str,
        card_id: int,
        device_id: int,
        parser: AlsaStreamInfoParser,
    ) -> JackAlsaDevice:
        """Creates a JACK ALSA terminal device."""

        assert isinstance(name, str) and name.strip()
        assert 0 <= card_id
        assert 0 == device_id, "Currently only 'device_id == 0' supported."
        assert isinstance(parser, AlsaStreamInfoParser)

        return JackAlsaDevice(name, card_id, device_id, parser)

    @staticmethod
    def create_mixbus(
        name: str,
        channel_count: int = 2
    ) -> JackBusDevice:
        """Creates a JACK mixbus device."""

        assert isinstance(name, str) and name.strip()
        assert isinstance(channel_count, int) and 0 < channel_count

        result: JackBusDevice = JackBusDevice(name, channel_count)

        return result

    @staticmethod
    def create_mixbus_group() -> list[JackBusDevice]:
        """Creates a JACK mixbus device group."""

        result: list[JackBusDevice] = []

        mx0 = JackBusDevice(MixbusDevice.MX0.name).acquire()
        mx1 = JackBusDevice(MixbusDevice.MX1.name,
                            channel_count=len(IsoChannelDry)).acquire()
        mx2 = JackBusDevice(MixbusDevice.MX2.name,
                            channel_count=len(IsoChannelWet)).acquire()
        mx3 = JackBusDevice(MixbusDevice.MX3.name).acquire()
        mx4 = JackBusDevice(MixbusDevice.MX4.name).acquire()
        mx5 = JackBusDevice(MixbusDevice.MX5.name).acquire()
        mx6 = JackBusDevice(MixbusDevice.MX6.name).acquire()

        dr0 = JackBusDevice(MixbusDevice.DR0.name).acquire()
        wt0 = JackBusDevice(MixbusDevice.WT0.name).acquire()
        dr1 = JackBusDevice(MixbusDevice.DR1.name).acquire()
        wt1 = JackBusDevice(MixbusDevice.WT1.name).acquire()
        dr2 = JackBusDevice(MixbusDevice.DR2.name).acquire()
        wt2 = JackBusDevice(MixbusDevice.WT2.name).acquire()

        # NOTE: mx0 (the master/mix-down bus) is fed from the WET channel
        # strips, not the raw DRY ones: WT0/WT1/WT2 already fall back to a
        # pass-through copy of DR0/DR1/DR2 whenever no external effect
        # hardware is present (see the DR0->WT0 / DR2->WT2 passthroughs
        # below, and SkippingIn1), so the master always reflects dry
        # content when no real WET information exists, and the actual
        # processed signal when it does. mx3/mx4/mx5/mx6 are per-performer
        # monitor/foldback buses routed out to headset hardware (see
        # DetectingLcl/DetectingEx1/DetectingEx2); they must NOT be routed
        # back into mx0, or the master (and, via mx0, the MST_LEFT/
        # MST_RIGHT reference tracks copied into MX1 and MX2) ends up with
        # duplicated DRY and WET content (issue #89).
        wt0.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        wt1.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        wt2.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)

        dr0.connect_to(wt0.as_sink_set(), ConnectionPolicy.DUAL)

        # NOTE: This connection will be removed, and created in
        # SkippingIn2.
        dr2.connect_to(wt2.as_sink_set(), ConnectionPolicy.DUAL)

        dr2.connect_to(mx3.as_sink_set(), ConnectionPolicy.DUAL)
        wt1.connect_to(mx3.as_sink_set(), ConnectionPolicy.DUAL)

        dr0.connect_to(mx4.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(mx4.as_sink_set(), ConnectionPolicy.DUAL)

        dr0.connect_to(mx5.as_sink_set(), ConnectionPolicy.DUAL)
        wt1.connect_to(mx5.as_sink_set(), ConnectionPolicy.DUAL)

        mx0.connect_to(mx1.as_sink_set(), ConnectionPolicy.DUAL)
        dr0.sources[IsoChannelDry.MST_LEFT].connect_to(
            mx1.sinks[IsoChannelDry.DR0_LEFT])
        dr0.sources[IsoChannelDry.MST_RIGHT].connect_to(
            mx1.sinks[IsoChannelDry.DR0_RIGHT])
        dr1.sources[IsoChannelDry.MST_LEFT].connect_to(
            mx1.sinks[IsoChannelDry.DR1_LEFT])
        dr1.sources[IsoChannelDry.MST_RIGHT].connect_to(
            mx1.sinks[IsoChannelDry.DR1_RIGHT])
        dr2.sources[IsoChannelDry.MST_LEFT].connect_to(
            mx1.sinks[IsoChannelDry.DR2_LEFT])
        dr2.sources[IsoChannelDry.MST_RIGHT].connect_to(
            mx1.sinks[IsoChannelDry.DR2_RIGHT])

        mx0.connect_to(mx2.as_sink_set(), ConnectionPolicy.DUAL)
        wt0.sources[IsoChannelWet.MST_LEFT].connect_to(
            mx2.sinks[IsoChannelWet.WT0_LEFT])
        wt0.sources[IsoChannelWet.MST_RIGHT].connect_to(
            mx2.sinks[IsoChannelWet.WT0_RIGHT])
        wt1.sources[IsoChannelWet.MST_LEFT].connect_to(
            mx2.sinks[IsoChannelWet.WT1_LEFT])
        wt1.sources[IsoChannelWet.MST_RIGHT].connect_to(
            mx2.sinks[IsoChannelWet.WT1_RIGHT])
        wt2.sources[IsoChannelWet.MST_LEFT].connect_to(
            mx2.sinks[IsoChannelWet.WT2_LEFT])
        wt2.sources[IsoChannelWet.MST_RIGHT].connect_to(
            mx2.sinks[IsoChannelWet.WT2_RIGHT])

        result.append(mx0)
        result.append(mx1)
        result.append(mx2)
        result.append(mx3)
        result.append(mx4)
        result.append(mx5)
        result.append(mx6)
        result.append(dr0)
        result.append(wt0)
        result.append(dr1)
        result.append(wt1)
        result.append(dr2)
        result.append(wt2)

        return result
