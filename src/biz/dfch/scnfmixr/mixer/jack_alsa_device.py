# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

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

"""Module signal_point."""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import cast, Self
from threading import Lock

from biz.dfch.logging import log


import biz.dfch.scnfmixr.public.mixer.signal_point as pt
from ..public.mixer import Connection
from ..public.mixer import IAcquirable

from ..system import MessageQueue
from ..public.messages import MessageBase, Topology
from ..jack_commands import AlsaToJack, JackToAlsa

from ..alsa_usb import (
    AlsaStreamInfoParser,
)

from ..public.mixer import ConnectionInfo
from ..public.audio import (
    AlsaInterfaceInfo,
    Format,
    SampleRate,
    Constant,
)


__all__ = [
    "JackAlsaDevice",
]


class AlsaDevice(pt.ITerminalDevice):
    """Represents an ALSA audio device."""


class AcquirableDeviceMixin(IAcquirable, ABC):
    """JackAlsaDeviceAcquirableMixin"""

    _is_acquired: bool
    _mq: MessageQueue

    def __init__(self):
        super().__init__()

        self._is_acquired = False
        self._mq = MessageQueue.Factory.get()

    def acquire(self) -> Self:
        if self._is_acquired:
            return self

        try:
            log.debug("Acquiring resource ...")

            self._mq.register(
                self._on_message,
                lambda e: isinstance(e, Topology.ChangedNotification))

            result = self._do_acquire()

            self._is_acquired = True

            log.info("Acquiring resource OK.")

            return result

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(Topology.DeviceErrorNotification(self.name))
            log.error("Acquiring resource FAILED. [%s]", ex, exc_info=True)

    def release(self) -> None:

        if not self._is_acquired:
            return

        try:
            log.debug("Releasing resource ...")

            self._do_release()

            self._mq.unregister(self._on_message)

            log.info("Releasing resource OK.")

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(Topology.DeviceErrorNotification(self.name))
            log.error("Releasing resource FAILED. [%s]", ex, exc_info=True)

    @abstractmethod
    def _do_acquire(self) -> Self:
        """Actual acquisition implementation."""

        raise NotImplementedError

    @abstractmethod
    def _do_release(self):
        """Actual release implementation."""

        raise NotImplementedError

    @abstractmethod
    def _on_message(self, message: MessageBase):
        """Message handler."""

        raise NotImplementedError


class PointState(Enum):
    """The states of a point."""
    INITIAL = 0
    OK = 1
    STALE = 2
    REMOVED = 3


class SourceOrSinkPoint(pt.IConnectablePoint, AcquirableDeviceMixin):
    """Represents a source or sink point."""

    _state: PointState
    _info: ConnectionInfo

    def __init__(self, name: str, info: ConnectionInfo):
        super().__init__(name)

        assert isinstance(name, str) and name.strip()
        assert isinstance(info, ConnectionInfo)

        self._state = PointState.INITIAL
        self._info = info

    @property
    def is_active(self):
        return self._state == PointState.OK

    def _do_acquire(self):
        # Nothing to do here.
        return self

    def _do_release(self):
        self._state = PointState.REMOVED

    def _on_message(self, message):
        return


class SourcePoint(
    SourceOrSinkPoint,
    pt.IConnectableSourcePoint,
    AcquirableDeviceMixin
):
    """Represents a source point."""

    @property
    def is_sink(self):
        return False

    def connect_to(self, other):
        raise NotImplementedError


class SinkPoint(
    SourceOrSinkPoint,
    pt.IConnectableSinkPoint,
    AcquirableDeviceMixin
):
    """Represents a sink point."""

    @property
    def is_source(self):
        return False

    def connect_to(self, other):
        raise NotImplementedError


class TerminalSourcePoint(
        SourcePoint,
        pt.ITerminalSourcePoint,
        AcquirableDeviceMixin):
    """Represents a terminal source point."""


class TerminalSinkPoint(
        SinkPoint,
        pt.ITerminalSinkPoint,
        AcquirableDeviceMixin):
    """Represents a terminal sink point."""


class JackAlsaDevice(AlsaDevice, AcquirableDeviceMixin):
    """Represents a JACK ALSA audio device."""

    _mq: MessageQueue
    _sync_root: Lock
    _info: ConnectionInfo
    _source_bridge: AlsaToJack | None
    _source_client: str | None
    _sink_bridge: JackToAlsa | None
    _sink_client: str | None

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
                of the ALSA  card and device.
        """
        super().__init__(Connection.jack_client_name_from_basename(name))

        assert isinstance(name, str) and name.strip()
        assert 0 <= card_id
        assert 0 == device_id, "Currently only 'device_id == 0' supported."
        assert isinstance(parser, AlsaStreamInfoParser)

        self._sync_root = Lock()
        self._mq = MessageQueue.Factory.get()

        self._info = ConnectionInfo({})
        self._source_bridge = None
        self._sink_bridge = None
        self._source_client = None
        self._sink_client = None

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

        assert isinstance(message, MessageBase)

        if not isinstance(message, Topology.ChangedNotification):
            return

        if not isinstance(message.value, ConnectionInfo):
            return

        self._info = message.value

        items = self._info.get_sources(self._source_client)
        log.debug("Device '%s'. Sources: [%s]", self._source_client, items)

        self._update_points_state(items, self.sources)

        items = self._info.get_sinks(self._sink_client)
        log.debug("Device '%s'. Sinks: [%s]", self._sink_client, items)

        self._update_points_state(items, self.sinks)

    def _update_points_state(
            self,
            items: list[str],
            points: list[SourceOrSinkPoint]):
        """Updates point status."""

        for point_ in points:

            point = cast(SourceOrSinkPoint, point_)
            match point._state:
                case PointState.INITIAL:
                    if point.name in items:
                        point._state = PointState.OK
                        self._mq.publish(
                            Topology.PointAddedNotification(point.name))
                        log.debug("Point '%s' is [%s]",
                                  point.name, point._state.name)
                        continue
                case PointState.OK:
                    if point.name not in items:
                        point._state = PointState.STALE
                        self._mq.publish(
                            Topology.PointLostNotification(point.name))
                        log.debug("Point '%s' is [%s]",
                                  point.name, point._state.name)
                        continue
                case PointState.STALE:
                    if point.name in items:
                        point._state = PointState.OK
                        self._mq.publish(
                            Topology.PointFoundNotification(point.name))
                        log.debug("Point '%s' is [%s]",
                                  point.name, point._state.name)
                        continue
                case _:
                    log.warning("Point '%s' is [%s]",
                                point.name, point._state.name)
                    continue

    def _do_acquire(self):

        self._mq.publish(Topology.DeviceAddingNotification(self.name))

        self._source_client = Connection.jack_client_name_source_prefix(
            self._logical_name)
        self._source_bridge = AlsaToJack(
            self._source_client,
            self._device_name,
            self._best_source_interface.channel_count,
            self._best_source_interface.sample_rate.value)

        items = Connection.get_jack_source_port_names(
            self._best_source_interface.channel_count, self._source_client)
        for item in items:

            log.debug("Creating source point '%s' ...", item)
            self._mq.publish(Topology.PointAddingNotification(item))
            point = TerminalSourcePoint(item, self._info)  # pylint: disable=E0110  # noqa: E501
            self.add(point)
            point.acquire()
            log.debug(("Creating source point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

        self._sink_client = Connection.jack_client_name_sink_prefix(
            self._logical_name)
        self._sink_bridge = JackToAlsa(
            self._sink_client,
            self._device_name,
            self._best_sink_interface.channel_count,
            self._best_sink_interface.sample_rate.value)

        items = Connection.get_jack_sink_port_names(
            self._best_sink_interface.channel_count, self._sink_client)
        for item in items:

            log.debug("Creating sink point '%s' ...", item)
            self._mq.publish(Topology.PointAddingNotification(item))
            point = TerminalSinkPoint(item, self._info)  # pylint: disable=E0110  # noqa: E501
            self.add(point)
            point.acquire()
            log.debug(("Creating sink point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

        self._mq.publish(Topology.DeviceAddedNotification(self.name))

    def _do_release(self):

        self._mq.publish(Topology.DeviceRemovingNotification(self.name))

        for point in self.sources:
            log.debug(
                "Removing source point '%s' on device '%s' ...",
                point.name,
                self.name)
            self._mq.publish(Topology.PointRemovingNotification(point.name))

            point.release()

        self._source_bridge.stop()
        self._source_bridge = None

        for i in reversed(range(len(self.sources))):
            point = self.sources[i]

            log.debug(
                "Removing source point '%s' on device '%s' OK.",
                point.name,
                self.name)
            self._mq.publish(Topology.PointRemovedNotification(point.name))
            del self.sources[i]

        for point in self.sinks:
            log.debug(
                "Removing sink point '%s' on device '%s' ...",
                point.name,
                self.name)
            self._mq.publish(Topology.PointRemovingNotification(point.name))

            point.release()

        self._sink_bridge.stop()
        self._sink_bridge = None

        for i in reversed(range(len(self.sinks))):
            point = self.sinks[i]

            log.debug(
                "Removing sink point '%s' on device '%s' OK.",
                point.name,
                self.name)
            self._mq.publish(Topology.PointRemovedNotification(point.name))
            del self.sinks[i]

        self._mq.publish(Topology.DeviceRemovedNotification(self.name))

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def points(self):
        return self._items.keys()
