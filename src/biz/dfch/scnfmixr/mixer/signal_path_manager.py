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

"""Module signal_path_manager."""

from __future__ import annotations
import logging
import time
from dataclasses import dataclass
from threading import Event, Lock, Thread
from typing import ClassVar


# May better to implement a factory on ~Manager. That way we do not have to
# pass info back from SignalPath to the mgr.
from biz.dfch.logging import log
from biz.dfch.scnfmixr.jack_commands import JackConnection
from biz.dfch.scnfmixr.public.messages import (
    AudioMixer,
    MessageBase,
    SystemMessage,
    Topology,
)
from biz.dfch.scnfmixr.public.mixer import (
    ConnectionInfo,
    IConnectableSinkPoint,
    IConnectableSourcePoint,
)
from biz.dfch.scnfmixr.system import MessageQueue


class SignalPathManager:
    """Manages all signal paths."""

    @dataclass(frozen=True)
    class Connection:
        """Connection details."""
        source: IConnectableSourcePoint
        sink: IConnectableSinkPoint

        def __eq__(self, other):

            if not isinstance(other, SignalPathManager.Connection):
                return NotImplemented

            return (self.source.name == other.source.name
                    and self.sink.name == other.sink.name)

        def __hash__(self):
            return hash((self.source.name, self.sink.name))

    _sync_root: Lock

    @dataclass
    class ConnectionInfo:
        """Contains information about a JACK connection."""
        conn: SignalPathManager.Connection
        jack: JackConnection

    _WAIT_INTERVAL_S: int = 1
    _KEEP_ALIVE_INTERVAL_S = 10

    _sync_root: Lock
    _items: list[SignalPathManager.ConnectionInfo]
    _is_processing_paused: bool
    _mq: MessageQueue
    _signal_stop: Event
    _worker_thread: Thread

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not SignalPathManager.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._sync_root = Lock()
        self._items = list[SignalPathManager.ConnectionInfo]()

        self._is_processing_paused = False
        self._mq = MessageQueue.Factory.get()
        self._mq.register(
            self._on_message,
            lambda e: isinstance(e, (
                AudioMixer.StoppedNotification,
                AudioMixer.StartedNotification,
                SystemMessage.Shutdown)))

        self._signal_stop = Event()
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

        log.info("Initialising OK.")

    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

        if isinstance(message, SystemMessage.Shutdown):
            self._signal_stop.set()
            return

        if isinstance(message, AudioMixer.StoppedNotification):
            self._is_processing_paused = True

        if isinstance(message, AudioMixer.StartedNotification):
            self._is_processing_paused = False

    class SuppressDebugMultiLineTextParser(logging.Filter):
        """Supress DEBUG level logging of module MultiLineTextParser."""

        def filter(self, record) -> bool:

            if (record.levelno == logging.DEBUG
                    and record.module == "MultiLineTextParser"):
                return False
            return True

    def _worker(self) -> None:
        """Worker continuously getting JACK connections."""

        log.debug("_worker: Initialising ...")

        previous: dict[tuple[str, bool], list[str]] = {}
        start = time.monotonic()
        log_filter = SignalPathManager.SuppressDebugMultiLineTextParser()

        log.info("_worker: Initialising OK.")

        log.debug("_worker: Processing ...")

        while not self._signal_stop.wait(self._WAIT_INTERVAL_S):

            try:

                now = time.monotonic()
                if now > start + self._KEEP_ALIVE_INTERVAL_S:
                    start = now
                    log.debug(
                        "_worker: Keep alive%s.",
                        (" [paused]" if self._is_processing_paused else ""))

                if self._is_processing_paused:
                    continue

                # DFTODO: Quirky and not thread safe. Maybe subclass and lock?
                log.addFilter(log_filter)
                result = JackConnection.get_connections3()
                log.removeFilter(log_filter)

                if previous == result:
                    continue

                previous = result

                connection_info = ConnectionInfo(result)
                assert connection_info

                self._mq.publish(Topology.ChangedNotification(connection_info))

                log.debug("Topology changed: %s", connection_info)

            except Exception as ex:  # pylint: disable=W0718

                log.error("_worker: An exception occurred. [%s]",
                          ex, exc_info=True)

        log.info("_worker: Processing stopped.")

    def add(
            self,
            conn: SignalPathManager.Connection,
    ) -> bool:
        """Adds a connection to the manager."""

        assert isinstance(conn, SignalPathManager.Connection)
        assert isinstance(conn.source, IConnectableSourcePoint)
        assert isinstance(conn.sink, IConnectableSinkPoint)

        with self._sync_root:

            if self._is_active(conn):
                return True

            item = next((e for e in self._items if e.conn == conn), None)
            assert item

        # if self._is_active(conn):
        #     return True

        # self._sync_root.acquire_lock()

        #     if self._is_active(conn):
        #         return True

    def remove(
            self,
            conn: SignalPathManager.Connection,
    ) -> bool:
        """Removes a connection from the manager."""

        assert isinstance(conn, SignalPathManager.Connection)
        assert isinstance(conn.source, IConnectableSourcePoint)
        assert isinstance(conn.sink, IConnectableSinkPoint)

        with self._sync_root:

            if not self._is_active(conn):
                return True

            item = next((e for e in self._items if e.conn == conn), None)
            assert item

    def _is_active(
            self,
            conn: SignalPathManager.Connection,
    ) -> bool:
        """Internal: Determines whether a connection exist and is active."""

        return any(e.conn == conn for e in self._items)

    def is_active(
            self,
            conn: SignalPathManager.Connection,
    ) -> bool:
        """Determines whether a connection exist and is active."""

        assert isinstance(conn, SignalPathManager.Connection)
        assert isinstance(conn.source, IConnectableSourcePoint)
        assert isinstance(conn.sink, IConnectableSinkPoint)

        with self._sync_root:
            return self._is_active(conn)

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[SignalPathManager | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> "SignalPathManager":
            """Creates or gets the instance of the SignalPathManager."""

            if SignalPathManager.Factory.__instance is not None:
                return SignalPathManager.Factory.__instance

            with SignalPathManager.Factory._sync_root:

                if SignalPathManager.Factory.__instance is not None:
                    return SignalPathManager.Factory.__instance

                SignalPathManager.Factory.__instance = SignalPathManager()

            return SignalPathManager.Factory.__instance
