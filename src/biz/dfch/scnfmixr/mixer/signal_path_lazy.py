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

from biz.dfch.scnfmixr.public.messages import Topology
from biz.dfch.scnfmixr.public.mixer import (
    IAcquirable,
    ISignalPath,
    IConnectableSink,
    IConnectableSinkPoint,
    IConnectableSource,
    IConnectableSourcePoint,
    PathState,
    PathStateFlag
)
from biz.dfch.scnfmixr.system import MessageQueue


class SignalPathLazy(ISignalPath, IAcquirable):
    """A lazy signal path implementation."""

    _mq: MessageQueue
    _source: IConnectableSource
    _sink: IConnectableSink
    _state: PathState

    def __init__(
            self,
            source: IConnectableSourcePoint,
            sink: IConnectableSinkPoint,
            state: PathState
    ) -> None:

        super().__init__(source, sink)

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)
        assert isinstance(state, PathState)

        self._mq = MessageQueue.Factory.get()
        self._source = source
        self._sink = sink
        self._state = state

    def acquire(self):
        if self._state.is_acquired:
            return self

        self._mq.publish(Topology.PathConnectingNotification(self.name))

        self._state.value = PathStateFlag.INITIAL
        self._state.is_acquired = True
        return self

    def release(self):
        if not self._state.is_acquired:
            return

        self._mq.publish(Topology.PathDisconnectingNotification(self.name))

        self._state.value = PathStateFlag.REMOVED
        self._state.is_acquired = False

    @property
    def is_active(self):
        return (self._state.is_acquired and
                self._state.has_flag(PathStateFlag.OK))
