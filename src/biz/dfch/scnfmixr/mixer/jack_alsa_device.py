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

"""Module jack_alsa_device."""

from __future__ import annotations
from threading import Lock
from typing import cast

from biz.dfch.logging import log
from biz.dfch.asyn import Retry, ThreadPool

from ..public.mixer import Connection, ConnectionInfo, ConnectionPolicy

from ..system import MessageQueue
from ..public.messages import MessageBase, Topology
from ..jack_commands import AlsaToJack, JackToAlsa

from ..alsa_usb import (
    AlsaStreamInfoParser,
)

from ..public.audio import (
    AlsaInterfaceInfo,
    Format,
    SampleRate,
    Constant,
)

from .acquirable_device_mixin import AcquirableDeviceMixin
from .alsa_device import AlsaDevice
from .jack_signal_manager import JackSignalManager


__all__ = [
    "JackAlsaDevice",
]


class JackAlsaDevice(AlsaDevice, AcquirableDeviceMixin):
    """Represents a JACK ALSA audio device."""

    _sync_root: Lock
    _mq: MessageQueue
    _mgr: JackSignalManager
    _info: ConnectionInfo
    _source_bridge: AlsaToJack | None
    _source_client_name: str | None
    _sink_bridge: JackToAlsa | None
    _sink_client_name: str | None

    _logical_name: str
    _card_id: int
    _device_id: int
    _device_name: str

    _best_source_interface: AlsaInterfaceInfo
    _best_sink_interface: AlsaInterfaceInfo

    def __init__(
            self,
            name: str,
            card_id: int,
            device_id: int,
            parser: AlsaStreamInfoParser,
    ) -> None:
        """Createa JackAlsaDevice.

        Args:
            name (str): The logical name the ALSA card (eg. `LCL`, `EX1`,
                `EX2`).
            card_id (int): Id of the ALSA card (starting at `0`).
            device_id (int): Id of the ALSA device (starting at `0`).
            parser (AlsaStramInfoParser): An instance to the stream info parser
                of the ALSA card and device.
        """
        super().__init__(Connection.jack_alsa_client_from_base(name))

        assert isinstance(name, str) and name.strip()
        assert 0 <= card_id
        assert 0 == device_id, "Currently only 'device_id == 0' supported."
        assert isinstance(parser, AlsaStreamInfoParser)

        self._sync_root = Lock()
        self._mq = MessageQueue.Factory.get()

        self._mgr = JackSignalManager.Factory.get()

        self._info = ConnectionInfo({})
        self._source_bridge = None
        self._sink_bridge = None
        self._source_client_name = None
        self._sink_client_name = None

        self._logical_name = name
        self._card_id = card_id
        self._device_id = device_id
        self._device_name = Constant.get_raw_device_name(card_id, device_id)

        log.debug("Validating stream information for '%s' [%s] ...",
                  self.name, self._device_name)

        iface = parser.get_best_capture_interface()
        log.debug("Selected capture interface. [%s]", iface)

        self._best_source_interface = AlsaInterfaceInfo(
            card_id=self._card_id,
            interface_id=parser.interface_id,
            channel_count=iface.channel_count,
            format=Format(iface.format),
            bit_depth=Format(iface.format).get_bit_depth(),
            sample_rate=SampleRate(iface.get_best_rate()),
        )
        log.debug("Selected source interface. [%s]",
                  self._best_source_interface)

        iface = parser.get_best_playback_interface()
        log.debug("Selected playback interface. [%s]", iface)

        self._best_sink_interface = AlsaInterfaceInfo(
            card_id=self._card_id,
            interface_id=parser.interface_id,
            channel_count=iface.channel_count,
            format=Format(iface.format),
            sample_rate=SampleRate(iface.get_best_rate()),
            bit_depth=Format(iface.format).get_bit_depth(),
        )
        log.debug("Selected sink interface. [%s]", self._best_sink_interface)

    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

        name = cast(Topology.PointLostNotification, message).value

        if not any(name == e.name for e in self.points):
            return

        point = next(e for e in self.points if e.name == name)

        tp = ThreadPool.Factory.get()
        rt = Retry(spin_attempts=25,
                   description=name)
        if not point.is_sink:
            log.warning("Lost source point notified: '%s'.", name)
            tp.invoke(rt.invoke, self._recreate_source_bridge, name)
        else:
            log.warning("Lost sink point notified: '%s'.", name)
            tp.invoke(rt.invoke, self._recreate_sink_bridge, name)

        return False

    def _recreate_source_bridge(self, name: str) -> bool:
        """Recreates the ALSA JACK source bridge."""

        assert isinstance(name, str) and name.strip()

        point = next((e for e in self.sources if e.name == name), None)
        assert point is not None, name

        if point.state.has_flag(point.state.Flag.OK):
            return True

        self._source_bridge = AlsaToJack(
            self._source_client_name,
            self._device_name,
            self._best_source_interface.channel_count,
            self._best_source_interface.sample_rate.value)

        return False

    def _recreate_sink_bridge(self, name: str) -> bool:
        """Recreates the ALSA JACK sink bridge."""

        assert isinstance(name, str) and name.strip()

        point = next((e for e in self.sinks if e.name == name), None)
        assert point is not None, name

        if point.state.has_flag(point.state.Flag.OK):
            return True

        self._sink_bridge = JackToAlsa(
            self._sink_client_name,
            self._device_name,
            self._best_sink_interface.channel_count,
            self._best_sink_interface.sample_rate.value)

        return False

    def do_acquire(self):

        self._source_client_name = Connection.jack_alsa_client_source_prefix(  # noqa: E501
            self._logical_name)
        self._source_bridge = AlsaToJack(
            self._source_client_name,
            self._device_name,
            self._best_source_interface.channel_count,
            self._best_source_interface.sample_rate.value)

        items = Connection.get_jack_source_port_names(
            self._best_source_interface.channel_count, self._source_client_name)
        for item in items:

            log.debug("Creating source point '%s' ...", item)
            point = self._mgr.get_jack_terminal_source_point(
                item, self._info)
            self.add(point)
            point.acquire()
            log.debug(("Creating source point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

        self._sink_client_name = Connection.jack_alsa_client_sink_prefix(
            self._logical_name)
        self._sink_bridge = JackToAlsa(
            self._sink_client_name,
            self._device_name,
            self._best_sink_interface.channel_count,
            self._best_sink_interface.sample_rate.value)

        items = Connection.get_jack_sink_port_names(
            self._best_sink_interface.channel_count, self._sink_client_name)
        for item in items:

            log.debug("Creating sink point '%s' ...", item)
            point = self._mgr.get_jack_terminal_sink_point(
                item, self._info)
            self.add(point)
            point.acquire()
            log.debug(("Creating sink point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

    def do_release(self):

        for point in self.sources:
            log.debug(
                "Releasing source point '%s' on device '%s' ...",
                point.name,
                self.name)

            point.release()

            for _, value in self._mgr.path_information.items():
                _, path = value
                if (
                    path.source.name != point.name
                    and path.sink.name != point.name
                ):
                    continue

                path.release()
                break

        self._source_bridge.stop()
        self._source_bridge = None

        for i in reversed(range(len(self.sources))):
            point = self.sources[i]

            log.debug(
                "Removing source point '%s' on device '%s' OK.",
                point.name,
                self.name)
            del self.sources[i]

        for point in self.sinks:
            log.debug(
                "Releasing sink point '%s' on device '%s' ...",
                point.name,
                self.name)

            point.release()

            for _, value in self._mgr.path_information.items():
                _, path = value
                if (
                    path.source.name != point.name
                    and path.sink.name != point.name
                ):
                    continue

                path.release()
                break

        self._sink_bridge.stop()
        self._sink_bridge = None

        for i in reversed(range(len(self.sinks))):
            point = self.sinks[i]

            log.debug(
                "Removing sink point '%s' on device '%s' OK.",
                point.name,
                self.name)
            del self.sinks[i]

    @property
    def points(self):
        return self._items.keys()

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):

        result = self._mgr.get_signal_paths(
            self.as_source_set(), other, policy)

        for _, path in result:
            path.acquire()

        return result
