# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
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
    """Createa audio and mixer devices and device groups."""

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

        result: JackBusDevice = JackBusDevice(name, channel_count) \
            # pylint: disable=E0110

        return result

    @staticmethod
    def create_mixbus_group() -> list[JackBusDevice]:
        """Creates a JACK mixbus device group."""

        result: list[JackBusDevice] = []

        mx0 = JackBusDevice(MixbusDevice.MX0.name).acquire() \
            # pylint: disable=E0110
        mx1 = JackBusDevice(MixbusDevice.MX1.name,  # pylint: disable=E0110
                            channel_count=len(IsoChannelDry)).acquire()
        mx2 = JackBusDevice(MixbusDevice.MX2.name,  # pylint: disable=E0110
                            channel_count=len(IsoChannelWet)).acquire()
        mx3 = JackBusDevice(MixbusDevice.MX3.name).acquire() \
            # pylint: disable=E0110
        mx4 = JackBusDevice(MixbusDevice.MX4.name).acquire() \
            # pylint: disable=E0110
        mx5 = JackBusDevice(MixbusDevice.MX5.name).acquire() \
            # pylint: disable=E0110
        mx6 = JackBusDevice(MixbusDevice.MX6.name).acquire() \
            # pylint: disable=E0110

        dr0 = JackBusDevice(MixbusDevice.DR0.name).acquire() \
            # pylint: disable=E0110
        wt0 = JackBusDevice(MixbusDevice.WT0.name).acquire() \
            # pylint: disable=E0110
        dr1 = JackBusDevice(MixbusDevice.DR1.name).acquire() \
            # pylint: disable=E0110
        wt1 = JackBusDevice(MixbusDevice.WT1.name).acquire() \
            # pylint: disable=E0110
        dr2 = JackBusDevice(MixbusDevice.DR2.name).acquire() \
            # pylint: disable=E0110
        wt2 = JackBusDevice(MixbusDevice.WT2.name).acquire() \
            # pylint: disable=E0110

        dr0.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        dr1.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)

        mx3.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        mx4.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        mx5.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)
        mx6.connect_to(mx0.as_sink_set(), ConnectionPolicy.DUAL)

        dr0.connect_to(wt0.as_sink_set(), ConnectionPolicy.DUAL)
        dr1.connect_to(wt1.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(wt2.as_sink_set(), ConnectionPolicy.DUAL)

        dr1.connect_to(mx3.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(mx3.as_sink_set(), ConnectionPolicy.DUAL)
        dr0.connect_to(mx4.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(mx4.as_sink_set(), ConnectionPolicy.DUAL)
        dr0.connect_to(mx5.as_sink_set(), ConnectionPolicy.DUAL)
        dr2.connect_to(mx5.as_sink_set(), ConnectionPolicy.DUAL)

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
