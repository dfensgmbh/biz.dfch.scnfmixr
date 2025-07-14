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

"""Module audio_mixer."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from threading import Lock
from typing import ClassVar
from typing import Self
from typing import overload

from biz.dfch.logging import log
from ..public.mixer import Connection
from ..public.mixer import Input
from ..public.mixer import InputOrOutput

from ..public.audio import AudioDevice
from ..public.mixer import Constant


__all__ = [
    "AudioMixer",
]


# pylint: disable=R0903
class ConnectionStatus:
    """Status of a JACK connection."""

    def refresh(self) -> Self:
        """Refreshes the status of this instance."""

        # DFTODO - Perform the update.

        return self


@dataclass(frozen=True)
class RoutingMatrix:
    """The audio mixer routing matrix."""

    _mtx: dict[AudioDevice, dict[AudioDevice, ConnectionStatus]]

    def __init__(self):

        if not RoutingMatrix.Factory._lock.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initialising RoutingMatrix ...")

        object.__setattr__(self, "_mtx", {})

        log.debug("Initialising RoutingMatrix SUCCEEDED. [%s]", self._mtx)

    def add_input(self) -> bool:
        """Adds an input"""

    # pylint: disable=R0903
    class Factory:
        """Factory class."""

        __instance: ClassVar[RoutingMatrix | None] = None
        _lock: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> RoutingMatrix:
            """Gets the instance of the routing matrix."""

            if RoutingMatrix.Factory.__instance is not None:
                return RoutingMatrix.Factory.__instance

            with RoutingMatrix.Factory._lock:

                if RoutingMatrix.Factory.__instance is not None:
                    return RoutingMatrix.Factory.__instance

                RoutingMatrix.Factory.__instance = RoutingMatrix()

            return RoutingMatrix.Factory.__instance


class ChannelStripName(StrEnum):
    """Channel strip names."""

    GAIN = auto()
    HPF = auto()
    EQ = auto()
    COMP = auto()
    LIM = auto()


class AudioMixerConfiguration:
    """The AudioMixer configuration."""

    xputs: set[InputOrOutput]

    conns: set[Connection]

    def __init__(self):

        self.conns = set()
        self.xputs = set()

    def get_xput(self, name: str) -> InputOrOutput:
        """Gets an input or output based on its name from the configuration
        set."""

        assert name and name.strip()
        assert any(e.name == name for e in self.xputs)

        result = next((e for e in self.xputs if e.name == name), None)
        assert result is not None

        return result

    def get_input(self, name: str) -> Input:
        """Gets an input based on its name from the configuration set."""

        assert name and name.strip()
        actual_name = f"{name}{Constant.JACK_INFIX}{Constant.JACK_INPUT}"
        assert any(e.name == actual_name for e in self.xputs)

        result = self.get_xput(actual_name)

        return result

    def get_output(self, name: str) -> Input:
        """Gets an output based on its name from the configuration set."""

        assert name and name.strip()
        actual_name = f"{name}{Constant.JACK_INFIX}{Constant.JACK_OUTPUT}"
        assert any(e.name == actual_name for e in self.xputs)

        result = self.get_xput(actual_name)

        return result

    def add_xput(self, value: InputOrOutput) -> None:
        """Adds an input or ouput object to the configuration set."""

        assert value is not None
        assert value.name and value.name.strip()
        assert not any(e.name == value.name for e in self.xputs)

        log.debug("Adding object '%s' ...", value.name)

        self.xputs.add(value)

        log.info(
            "Adding object '%s' SUCCEEDED [%s].", value.name, len(self.xputs))

    def remove_xput(self, name: str) -> None:
        """Removes an input or ouput object from the configuration set."""

        assert name and name.strip()
        assert any(e.name == name for e in self.xputs)

        result = next((e for e in self.xputs if e.name == name), None)
        assert result is not None

        log.debug("Removing object '%s' ...", name)

        self.xputs.remove(result)

        log.info("Removing object '%s' SUCCEEDED [%s].", name, len(self.xputs))

    def add_connection(self, params: Connection) -> Self:
        """Adds a connection request."""

        assert params is not None

        self.conns.add(params)

        return self


class AudioMixerState(Enum):
    """The operational state of the audio mixer.

    Attributes:
        STOPPED: The service is stopped.
        STARTING: The service is starting.
        STARTED: The service is started.
        STOPPING: The service is stopping.
        ERROR: The service is in an error state.
    """

    STOPPED = auto()
    STARTING = auto()
    STARTED = auto()
    STOPPING = auto()
    ERROR = auto()


class AudioMixer:
    """The JACK audio mixer.

    Attributes:
    """

    _state: AudioMixerState
    _routing_matrix: RoutingMatrix
    _cfg: AudioMixerConfiguration

    # pylint: disable=R0903

    class Factory:
        """Factory class."""

        __instance: ClassVar[AudioMixer | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> AudioMixer:
            """Gets the instance of the audio mixer."""

            if AudioMixer.Factory.__instance is not None:
                return AudioMixer.Factory.__instance

            with AudioMixer.Factory._sync_root:

                if AudioMixer.Factory.__instance is not None:
                    return AudioMixer.Factory.__instance

                AudioMixer.Factory.__instance = AudioMixer()

            return AudioMixer.Factory.__instance

    def __init__(self):

        if not AudioMixer.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initialising AudioMixer ...")

        self._state = AudioMixerState.STOPPED
        self._routing_matrix = RoutingMatrix.Factory.get()
        self._cfg = None

        log.info("Initialising AudioMixer SUCCEEDED.")

    @overload
    def initialise(self) -> bool:
        ...

    @overload
    def initialise(self, cfg: AudioMixerConfiguration) -> bool:
        ...

    def initialise(self, cfg: AudioMixerConfiguration | None) -> bool:
        """Initialise the audio mixer. If the mixer has already been
        initialised, it will be re-initialised. Existing connections will be
        removed. Audio will temporarily stop.

        Args:
            cfg (AudioMixerConfiguration | None): The configuration to be
                initialised.

        Returns:
            bool: True, if the configuration was successfully initialised; false
                otherwise.
        """

        assert cfg is not None or isinstance(cfg, AudioMixerConfiguration)

        if self._cfg is not None:
            result = self.stop()
            assert result

        self._cfg = cfg

        result = self.start()

        return result

    @property
    def is_started(self) -> bool:
        """Determines whether the mixer is started.

        Returns:
            bool: True, if the mixer is started; false, otherwise.
        """

        return AudioMixerState.STARTED == self._state

    @property
    def state(self) -> AudioMixerState:
        """Returns the current state of the audio mixer.

        Returns:
            AudioMixerState: See `AudioMixerState` for description.
        """

        return self._state

    def start(self) -> bool:
        """Starts the audio mixer.

        Returns:
            bool: True, if the start command could be initiated; false,
                otherwise. Check `state` for actual state.
        """

        result = False

        if self._cfg is None:
            return result

        if AudioMixerState.STOPPED != self._state:
            return result

        for source in self._cfg.xputs:

            log.debug("Starting '%s' [%s] ...",
                      source.name, type(source).__name__)

            result = source.start()

            if result:
                log.info("Starting '%s' [%s] SUCCEEDED.",
                         source.name, type(source).__name__)
            else:
                log.error("Starting '%s' [%s] FAILED.",
                          source.name, type(source).__name__)

                self._state = AudioMixerState.ERROR
                return False

        for conn in self._cfg.conns:

            log.debug("Connecting '%s' [%s] to '%s' [%s] ...",
                      conn.this, conn.idx_this, conn.other, conn.idx_other)

            source = next(
                (xput for xput in self._cfg.xputs if xput.name == conn.this),
                None)
            if source is None:
                log.warning(
                    "Invalid connection parameters. '%s' does not exist. [%s]",
                    conn.this, conn)
                continue

            sink = next(
                (xput for xput in self._cfg.xputs if xput.name == conn.other),
                None)
            if sink is None:
                log.warning(
                    "Invalid connection parameters. '%s' does not exist. [%s]",
                    conn.other, conn)
                continue

            result = source.connect_to(sink, conn.idx_this, conn.idx_other)
            if not result:
                log.error("Connecting '%s' [%s] to '%s' [%s] FAILED.",
                          conn.this, conn.idx_this, conn.other, conn.idx_other)
                continue

            log.info("Connecting '%s' [%s] to '%s' [%s] SUCCEEDED.",
                     conn.this, conn.idx_this, conn.other, conn.idx_other)

        self._state = AudioMixerState.STARTED

        return result

    def stop(self) -> bool:
        """Stops the audio mixer.

        Returns:
            bool: True, if the stop command could be initiated; false,
                otherwise. Check `state` for actual state.
        """

        result = False

        if AudioMixerState.STARTED != self._state:
            return result

        for xput in self._cfg.xputs:

            log.debug("Stopping '%s' [%s] ...", xput.name, type(xput).__name__)

            result = xput.stop()

            if result:
                log.info("Stopping '%s' [%s] SUCCEEDED.",
                         xput.name, type(xput).__name__)
            else:
                log.error("Stopping '%s' [%s] FAILED.",
                          xput.name, type(xput).__name__)

                self._state = AudioMixerState.ERROR
                return False

        self._state = AudioMixerState.STOPPED

        return result

    def restart(self) -> bool:
        """Restarts the audio mixer.

        Returns:
            bool: True, if the start command could be initiated; false,
                otherwise. Check `state` for actual state.
        """

        self.stop()
        result = self.start()

        return result
