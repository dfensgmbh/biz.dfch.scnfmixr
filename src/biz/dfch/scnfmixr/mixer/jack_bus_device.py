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

"""Module signal_point."""

from __future__ import annotations
from threading import Lock

from biz.dfch.logging import log
from biz.dfch.asyn import ThreadPool, Process

from ..public.mixer import (
    Connection,
    ConnectionInfo,
    ConnectionPolicy,
    IConnectablePointOrSet,
    IConnectableDevice,
)

from ..system import MessageQueue
from ..public.messages import Topology

from ..public.audio import (
    Format,
    SampleRate,
)

from .acquirable_device_mixin import AcquirableDeviceMixin
from .jack_signal_manager import JackSignalManager

__all__ = [
    "JackBusDevice",
    "EcasoundCommandLineBuilder",
]


class EcasoundCommandLineBuilder:
    """Creates an ecasound command line for a mix bus device.

    See: http://nosignal.fi/ecasound/Documentation/ecasound_manpage.html
    """

    _ECASOUND_FULLNAME = '/usr/bin/ecasound'

    def create_bus(
        self,
        client: str,
        chain: str = "",
        encoding: Format = Format.F32_LE,
        channel_count: int = 2,
        sample_rate: SampleRate = SampleRate.R48000,
    ) -> list[str]:
        """Build an ecasound command line."""

        assert isinstance(client, str) and client.strip()
        assert isinstance(encoding, Format)
        assert isinstance(channel_count, int) and 0 < channel_count
        assert isinstance(sample_rate, SampleRate)

        if chain is None or not chain.strip():
            chain = client

        result = [
            self._ECASOUND_FULLNAME,
            # Scheduling priority SCHED_FIFO: 80
            '-r:80',
            # Buffer mode: realtime
            '-B:rt',
            '-q',
            f'-G:jack,":{client}",notransport',
            f'-a:"{chain}"',
            f'-f:{encoding.name.lower()},{channel_count},{sample_rate.value}',
            # LowCut / High-pass filter 80Hz
            '-efh:80',
            f'-i:jack,,{Connection.get_jack_sink_port_prefix()}',
            f'-o:jack,,{Connection.get_jack_source_port_prefix()}',
        ]

        return result


class JackBusDevice(IConnectableDevice, AcquirableDeviceMixin):
    """Represents a JACK ecasound mixbus device."""

    _logical_name: str
    _channel_count: int
    _source_client_name: str
    _sink_client_name: str

    _sync_root: Lock
    _mq: MessageQueue
    _mgr: JackSignalManager
    _info: ConnectionInfo
    _thread_pool: ThreadPool

    _process: Process | None

    def __init__(self, name, channel_count: int = 2):
        super().__init__(Connection.jack_mixbus_client_from_base(name))

        assert isinstance(name, str) and name.strip()
        assert isinstance(channel_count, int) and 0 < channel_count

        self._sync_root = Lock()
        self._mq = MessageQueue.Factory.get()
        self._mgr = JackSignalManager.Factory.get()
        self._info = ConnectionInfo({})
        self._thread_pool = ThreadPool.Factory.get()

        self._logical_name = name
        self._channel_count = channel_count
        self._source_client_name = ""
        self._sink_client_name = ""
        self._process = None

    def do_acquire(self):

        self._source_client_name = Connection.jack_mixbus_client_sink_prefix(  # noqa: E501 # pylint: disable=C0301
            self._logical_name)

        client = Connection.jack_mixbus_client_from_base(self._logical_name)
        cmd = EcasoundCommandLineBuilder().create_bus(
            client=client,
            channel_count=self._channel_count,
        )
        log.debug("cmd [%s]", cmd)
        _process = Process.start(
            cmd, wait_on_completion=False,
            capture_stdout=True,
            capture_stderr=True)

        log.debug("exit_code '%s'", _process.exit_code)
        log.debug("stdout '%s'", _process.stdout)
        log.debug("stderr '%s'", _process.stderr)

        items = Connection.get_jack_source_port_names(
            self._channel_count, client)
        for item in items:

            log.debug("Creating source point '%s' ...", item)
            point = self._mgr.get_jack_source_point(
                item, self._info)
            self.add(point)
            point.acquire()
            log.debug(("Creating source point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

        items = Connection.get_jack_sink_port_names(
            self._channel_count, client)
        for item in items:

            log.debug("Creating sink point '%s' ...", item)
            point = self._mgr.get_jack_sink_point(
                item, self._info)
            self.add(point)
            point.acquire()
            log.debug(("Creating sink point '%s' OK. "
                       "Need topology notification to reflect changes."), item)

        return self

    def do_release(self):

        for point in self.points:

            log.debug("Releasing point '%s' ...", point.name)

            point.release()

            log.info("Releasing point '%s' OK.", point.name)

            self.points.clear()

        if self._process is None:
            return

        self._process.stop(force=True)
        self._process = None

    def _on_message(self, message):

        if isinstance(message, Topology.PointLostNotification):
            pass

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):

        assert isinstance(other, IConnectablePointOrSet)
        assert isinstance(policy, ConnectionPolicy)

        result = self._mgr.get_signal_paths(
            self.as_source_set(), other, policy)

        for _, path in result:
            path.acquire()

        return result
