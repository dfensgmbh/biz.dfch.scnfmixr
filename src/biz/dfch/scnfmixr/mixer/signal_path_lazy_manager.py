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

"""Module signal_path."""

from __future__ import annotations
import threading
from threading import Event, Lock
from typing import Callable, ClassVar

from biz.dfch.logging import log
from biz.dfch.scnfmixr.public.messages import SystemMessage, Topology
from biz.dfch.scnfmixr.public.mixer import (
    ConnectionInfo,
    ConnectionPolicy,
    ConnectionPolicyException,
    IConnectableSink,
    IConnectableSource,
    ISignalPath,
    PathState,
)

from .acquirable_manager_mixin import AcquirableManagerMixin
from .path_creator import PathCreator


class SignalPathLazyManager(AcquirableManagerMixin):
    """A manager for lazy SignalPath."""

    PolicyFunction = Callable[
        [IConnectableSource, IConnectableSink],
        list[tuple[PathState, ISignalPath]]
    ]

    _signal: Event
    _signal_shutdown: Event
    _info: ConnectionInfo
    _paths: dict[str, tuple[PathState, ISignalPath]]

    def __init__(self):
        """Private ctor. Use Factory to create an instance of this object."""

        if not SignalPathLazyManager.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        super().__init__()

        self._sync_root = Lock()
        self._signal = Event()
        self._signal_shutdown = Event()
        self._info({})
        self._paths = {}

    def get_signal_paths(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
            policy: ConnectionPolicy,
    ) -> list[ISignalPath]:
        """Gets a path from source to sink."""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)
        assert isinstance(policy, ConnectionPolicy)

        result: list[tuple[PathState, ISignalPath]] = []

        creator = PathCreator(self._paths)
        policy_map: dict[
            ConnectionPolicy,
            SignalPathLazyManager.PolicyFunction
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

                for _, path in result:
                    key = path.name
                    if key not in self._paths:
                        self._paths[key] = path

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

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[SignalPathLazyManager | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

        @staticmethod
        def get() -> list[SignalPathLazyManager]:
            """Creates or gets signal path instances."""

            if SignalPathLazyManager.Factory.__instance is not None:
                return SignalPathLazyManager.Factory.__instance

            with SignalPathLazyManager.Factory._sync_root:

                if SignalPathLazyManager.Factory.__instance is not None:
                    return SignalPathLazyManager.Factory.__instance

                SignalPathLazyManager.Factory.__instance = (
                    SignalPathLazyManager()
                )

            return SignalPathLazyManager.Factory.__instance

    def do_acquire(self):
        raise NotImplementedError

    def do_release(self):
        raise NotImplementedError

    def _on_message(self, message):
        """Message handler."""

        if isinstance(message, Topology.ChangedNotification):

            with self._sync_root:
                assert isinstance(message.value, ConnectionInfo)
                self._info = message.value

            self._signal.set()

            return

        if isinstance(message, SystemMessage.Shutdown):

            self._signal_shutdown.set()

            return
