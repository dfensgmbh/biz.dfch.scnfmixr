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

"""Module signal_path_lazy_manager."""

from __future__ import annotations
import logging
import threading
from threading import Event, Lock, Thread
import time
from typing import Callable, ClassVar

from biz.dfch.logging import log
from biz.dfch.scnfmixr.jack_commands import JackConnection
from biz.dfch.asyn.thread_pool import ThreadPool
from biz.dfch.scnfmixr.public.messages import SystemMessage, Topology
from biz.dfch.scnfmixr.public.mixer import (
    ConnectionInfo,
    ConnectionPolicy,
    ConnectionPolicyException,
    IConnectablePoint,
    IConnectableSource,
    IConnectableSink,
    ISignalPath,
    State,
)

from .acquirable_manager_mixin import AcquirableManagerMixin
from .path_creator import PathCreator
from .jack_alsa_source_point import JackAlsaSourcePoint
from .jack_alsa_sink_point import JackAlsaSinkPoint


class JackSignalPointPathManager(AcquirableManagerMixin):
    """A manager for JACK connections."""

    PolicyFunction = Callable[
        [IConnectableSource, IConnectableSink],
        list[tuple[State, ISignalPath]]
    ]

    _WAIT_INTERVAL_S: int = 1
    _KEEP_ALIVE_INTERVAL_S = 10

    _thread_pool: ThreadPool

    _is_acquired: bool
    _sync_root: Lock
    _signal: Event
    _signal_shutdown: Event
    _info: ConnectionInfo
    _paths: dict[str, tuple[State, ISignalPath]]
    _points: dict[str, tuple[State, IConnectablePoint]]

    _worker_signal_stop: Event
    _worker_thread: Thread

    def __init__(self):
        """Private ctor. Use Factory to create an instance of this object."""

        if not JackSignalPointPathManager.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        super().__init__()

        self._thread_pool = ThreadPool.Factory.get()

        self._is_acquired = False
        self._sync_root = Lock()
        self._signal = Event()
        self._signal_shutdown = Event()
        self._info = {}
        self._paths = {}
        self._points = {}

        self._worker_signal_stop = Event()
        self._worker_thread = Thread(target=self._worker, daemon=True)

    class SuppressNoisyDebug(logging.Filter):
        """Supress DEBUG level logging of module MultiLineTextParser
        and process."""

        def filter(self, record) -> bool:

            if (record.levelno == logging.DEBUG
                    and record.module in ("MultiLineTextParser")):
                return False
            if (record.levelno in (logging.DEBUG, logging.INFO)
                    and record.module in ("process")):
                return False
            return True

    def _worker(self) -> None:
        """Worker continuously getting JACK connections."""

        log.debug("_worker: Initialising ...")

        previous: dict[tuple[str, bool], list[str]] = {}
        start = time.monotonic()
        log_filter = JackSignalPointPathManager.SuppressNoisyDebug()

        log.info("_worker: Initialising OK.")

        log.debug("_worker: Processing ...")

        while not self._worker_signal_stop.wait(self._WAIT_INTERVAL_S):

            try:
                now = time.monotonic()
                if now > start + self._KEEP_ALIVE_INTERVAL_S:
                    delta = now - start
                    start = now
                    log.debug("_worker: Keep alive [%sms].", int(delta*1000))

                # DFTODO: Quirky and not thread safe. Maybe subclass and lock?
                log.addFilter(log_filter)
                result = JackConnection.get_connections3()
                log.removeFilter(log_filter)

                if previous == result:
                    continue

                previous = result
                self._info = result

                connection_info = ConnectionInfo(result)
                assert connection_info

                self._mq.publish(
                    Topology.ChangedNotification(connection_info))
                log.debug("Topology changed: %s", connection_info)

                self._update_point_state(connection_info)
                self._update_path_state(connection_info)

            except Exception as ex:  # pylint: disable=W0718

                log.error("_worker: An exception occurred. [%s]",
                          ex, exc_info=True)

        log.info("_worker: Processing stopped.")

    def _update_path_state(self, topo: ConnectionInfo) -> None:
        """Updates path states."""

        assert isinstance(topo, ConnectionInfo)

        log.debug("Updating signal path states ...")

        with self._sync_root:

            for key, value in self._paths.items():

                state, path = value

                if not state.is_acquired:
                    log.debug(
                        "Skipped '%s'. Path '%s' not acquired.", key, path.name)
                    continue

                if not path.source.is_acquired:
                    log.debug(
                        "Skipped '%s'. Source '%s' not acquired.",
                        key, path.source.name)
                    continue

                if not path.sink.is_acquired:
                    log.debug(
                        "Skipped '%s'. Sink '%s' not acquired.",
                        key, path.sink.name)
                    continue

                if state.has_flag(State.Flag.INITIAL):
                    if topo.is_connected_to(path.source.name, path.sink.name):
                        state.set_flag(State.Flag.OK)
                        self._mq.publish(
                            Topology.PathConnectedNotification(key))
                    continue

                if state.has_flag(State.Flag.OK):
                    if not topo.is_connected_to(
                            path.source.name, path.sink.name):
                        state.set_flag(State.Flag.STALE)
                        self._mq.publish(Topology.PathLostNotification(key))
                    continue

                if state.has_flag(State.Flag.STALE):
                    if topo.is_connected_to(path.source.name, path.sink.name):
                        state.set_flag(State.Flag.OK)
                        self._mq.publish(Topology.PathFoundNotification(key))
                    continue

                if state.has_flag(State.Flag.REMOVED):
                    if topo.is_connected_to(path.source.name, path.sink.name):
                        self._mq.publish(Topology.PathZombieNotification(key))
                        log.warning(
                            "Path '%s' is REMOVED, but still active.", key)
                    continue

        log.info("Updating signal path states OK.")

    def _update_point_state(self, topo: ConnectionInfo) -> None:
        """Updates point topology information."""

        assert isinstance(topo, ConnectionInfo)

        log.debug("Updating signal point states ...")

        with self._sync_root:

            for key, value in self._points.items():

                state, point = value

                if not state.is_acquired:
                    log.debug(
                        "Skipped '%s'. Point '%s' not acquired.",
                        key, point.name)
                    continue

                if state.has_flag(State.Flag.INITIAL):
                    if topo.is_entry(point.name):
                        state.set_flag(State.Flag.OK)
                        self._mq.publish(
                            Topology.PointActivatedNotification(key))
                    continue

                if state.has_flag(State.Flag.OK):
                    if not topo.is_entry(point.name):
                        state.set_flag(State.Flag.STALE)
                        self._mq.publish(Topology.PointLostNotification(key))
                    continue

                if state.has_flag(State.Flag.STALE):
                    if topo.is_entry(point.name):
                        state.set_flag(State.Flag.OK)
                        self._mq.publish(Topology.PointFoundNotification(key))
                    continue

                if state.has_flag(State.Flag.REMOVED):
                    if topo.is_entry(point.name):
                        self._mq.publish(Topology.PointZombieNotification(key))
                        log.warning(
                            "Point '%s' is REMOVED, but still active.", key)
                    continue

        log.info("Updating signal point states OK.")

    @property
    def path_information(self) -> dict[str, tuple[State, ISignalPath]]:
        """Returns path information."""
        return self._paths

    def get_signal_paths(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
            policy: ConnectionPolicy,
    ) -> list[tuple[State, ISignalPath]]:
        """Gets a path from source to sink."""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)
        assert isinstance(policy, ConnectionPolicy)

        result: list[tuple[State, ISignalPath]] = []

        log.debug("Processing '%s' '%s' ...", source.name, sink.name)

        creator = PathCreator(self._paths)
        policy_map: dict[
            ConnectionPolicy,
            JackSignalPointPathManager.PolicyFunction
        ] = {
            ConnectionPolicy.MONO: creator.process_mono,
            ConnectionPolicy.DUAL: creator.process_dual,
            ConnectionPolicy.LINE: creator.process_line,
            ConnectionPolicy.BCAST: creator.process_bcast,
            ConnectionPolicy.MERGE: creator.process_merge,
            ConnectionPolicy.TRUNC: creator.process_trunc,
            ConnectionPolicy.DEFAULT: creator.process_default,
        }

        try:
            with self._sync_root:
                handler = policy_map.get(
                    policy,
                    policy_map[ConnectionPolicy.DEFAULT])
                result = handler(source, sink)

                for value in result:
                    _, path = value
                    key = path.name
                    if key not in self._paths:
                        self._paths[key] = value

        except ConnectionPolicyException as ex:
            log.warning("ConnectionPolicyException: "
                        "An exception occurred. [%s]",
                        ex, exc_info=True)
            return []

        except Exception as ex:  # pylint: disable=W0718
            log.error("An exception occurred. [%s]",
                      ex, exc_info=True)
            return []

        return result

    def get_source_point(
            self,
            name: str,
            info: ConnectionInfo
    ) -> JackAlsaSinkPoint:
        """Creates or gets the source point with the specified name."""

        assert isinstance(name, str) and name.strip()
        assert isinstance(info, ConnectionInfo)

        with self._sync_root:

            if name in self._points:
                return self._points[name]

            # Really weird, pylint complains about instantiated abstract class.
            # But the class can be instantiated at runtime.
            result = JackAlsaSourcePoint(name, info)  # pylint: disable=E0110

            self._points[name] = (result.state, result)

            return result

    def get_sink_point(
            self,
            name: str,
            info: ConnectionInfo
    ) -> JackAlsaSinkPoint:
        """Creates or gets the sink point with the specified name."""

        assert isinstance(name, str) and name.strip()
        assert isinstance(info, ConnectionInfo)

        with self._sync_root:

            if name in self._points:
                return self._points[name]

            # Really weird, pylint complains about instantiated abstract class.
            # But the class can be instantiated at runtime.
            result = JackAlsaSinkPoint(name, info)  # pylint: disable=E0110

            self._points[name] = (result.state, result)

            return result

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[JackSignalPointPathManager | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

        @staticmethod
        def get() -> JackSignalPointPathManager:
            """Gets the singleton."""

            if JackSignalPointPathManager.Factory.__instance is not None:
                return JackSignalPointPathManager.Factory.__instance

            with JackSignalPointPathManager.Factory._sync_root:

                if JackSignalPointPathManager.Factory.__instance is not None:
                    return JackSignalPointPathManager.Factory.__instance

                JackSignalPointPathManager.Factory.__instance = (
                    JackSignalPointPathManager()
                )

            return JackSignalPointPathManager.Factory.__instance

    def do_acquire(self):

        if self._is_acquired:
            return self

        self._worker_signal_stop.clear()
        self._worker_thread.start()

        self._is_acquired = True

    def do_release(self):

        if not self._is_acquired:
            return

        self._worker_signal_stop.set()

        self._is_acquired = False

    def _on_message(self, message):
        """Message handler."""

        # if isinstance(message, Topology.ChangedNotification):

        #     with self._sync_root:
        #         assert isinstance(message.value, ConnectionInfo)
        #         self._info = message.value

        #     self._signal.set()

        #     return

        if isinstance(message, SystemMessage.Shutdown):

            self._signal_shutdown.set()

            return

    @property
    def is_acquired(self):
        return self._is_acquired

    @is_acquired.setter
    def is_acquired(self, value):
        assert isinstance(value, bool)

        self._is_acquired = value
