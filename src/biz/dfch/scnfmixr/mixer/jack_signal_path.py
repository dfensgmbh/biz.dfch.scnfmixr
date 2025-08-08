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

"""Module signal_path_lazy."""

from biz.dfch.logging import log
from biz.dfch.asyn import Retry
from biz.dfch.scnfmixr.public.messages import Topology
from biz.dfch.scnfmixr.public.mixer import (
    IAcquirable,
    ISignalPath,
    IConnectableSink,
    IConnectableSinkPoint,
    IConnectableSource,
    IConnectableSourcePoint,
    State,
)
from biz.dfch.asyn.thread_pool import ThreadPool
from biz.dfch.scnfmixr.jack_commands import JackConnection
from biz.dfch.scnfmixr.system import MessageQueue
from biz.dfch.scnfmixr.public.messages import MessageBase


class JackSignalPath(ISignalPath, IAcquirable):
    """A JACK signal path implementation."""

    _thread_pool: ThreadPool
    _mq: MessageQueue
    _source: IConnectableSource
    _sink: IConnectableSink
    _state: State

    def __init__(
            self,
            source: IConnectableSourcePoint,
            sink: IConnectableSinkPoint,
            state: State
    ) -> None:

        super().__init__(source, sink)

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)
        assert isinstance(state, State)

        self._thread_pool = ThreadPool.Factory.get()
        self._mq = MessageQueue.Factory.get()
        self._source = source
        self._sink = sink
        self._state = state

    def _connect_path(self) -> bool:
        """Tries to connect a path."""

        if not self._state.is_acquired:
            log.warning(
                "Skipped '%s'. Trying to connect, but not acquired.",
                self.name)
            return True

        if self._state.has_flag(self._state.Flag.OK):
            log.info(
                "Completed '%s'. State '%s'.",
                self.name,
                self._state)
            return True

        log.debug("Trying to connect path from '%s' to '%s' ...",
                  self._source.name, self._sink.name)

        JackConnection.Factory().create(self._source.name, self._sink.name)

        log.info("Trying to connect path from '%s' to '%s' INVOKED.",
                 self._source.name, self._sink.name)

        return False

    def _reconnect_path(self) -> bool:
        """Tries to reconnect a path."""

        if not self._state.is_acquired:
            log.warning(
                "Skipped '%s'. Trying to reconnect, but not acquired.",
                self.name)
            return True

        if (
            # isinstance(self._source, IConnectableSourcePoint)
            # and not self._source.is_acquired
            not self._source.is_acquired
        ):
            log.warning(
                ("Skipped '%s'. Trying to reconnect, "
                 "but source '%s' not acquired."),
                self.name,
                self._source.name)
            return True

        if (
            # isinstance(self._sink, IConnectableSinkPoint)
            # and not self._sink.is_acquired
            not self._sink.is_acquired
        ):
            log.warning(
                ("Skipped '%s'. Trying to reconnect, "
                 "but sink '%s' not acquired."),
                self.name,
                self._sink.name)
            return True

        if not self._state.has_flag(self._state.Flag.STALE):
            log.info(
                "Completed '%s'. State '%s'.",
                self.name,
                self._state)
            return True

        log.warning("Trying to reconnect path from '%s' [%s] to '%s' [%s] ...",
                    self._source.name,
                    self._source.is_acquired,
                    self._sink.name,
                    self._sink.is_acquired
                    )

        JackConnection.Factory().create(self._source.name, self._sink.name)

        log.info("Trying to reconnect path from '%s' to '%s' INVOKED.",
                 self._source.name, self._sink.name)

        return False

    def _on_message(self, _: MessageBase):
        """Message handler."""

        self._thread_pool.invoke(
            Retry(base_wait_time_interval_ms=500,
                  description=self.name).invoke, self._reconnect_path)

    def acquire(self):
        if self._state.is_acquired:
            return self

        log.debug("Acquiring resource path '%s' ...", self.name)

        self._mq.publish(Topology.PathConnectingNotification(self.name))

        self._state.set_flag(State.Flag.INITIAL)
        self._state.is_acquired = True

        if not self._source.is_acquired or not self._sink.is_acquired:
            return self

        self._thread_pool.invoke(
            Retry(first_wait_time_ms=350,
                  base_wait_time_interval_ms=200,
                  spin_attempts=25,
                  description=self.name).invoke, self._connect_path)

        self._mq.register(
            self._on_message, lambda e: isinstance(
                e, Topology.PathLostNotification) and e.value == self.name)

        return self

    def release(self):
        if not self._state.is_acquired:
            return

        self._mq.publish(Topology.PathDisconnectingNotification(self.name))

        log.debug("Releasing resource path '%s' ...", self.name)

        self._state.set_flag(State.Flag.REMOVED)
        self._state.is_acquired = False

        self._mq.publish(Topology.PathDisconnectedNotification(self.name))

        self._mq.unregister(self._on_message)

    @property
    def is_active(self):
        return (self._state.is_acquired and
                self._state.has_flag(State.Flag.OK))

    @property
    def is_acquired(self):
        return self._state.is_acquired

    @is_acquired.setter
    def is_acquired(self, value):
        self._state.is_acquired = value
