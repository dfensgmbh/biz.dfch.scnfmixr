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
import threading
from typing import (
    ClassVar,
    Callable,
    Self,
    overload
)

from biz.dfch.logging import log
from biz.dfch.scnfmixr.mixer.mix_bus import Mixbus

from ..jack_commands import (
    JackClient,
    JackPort,
)
from ..system import MessageQueue
from ..public.messages import AudioMixer as msgt
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..public.mixer import (
    Connection,
    Input,
    InputOrOutput,
)
from ..public.audio import AudioDevice


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

        log.debug("Initialising RoutingMatrix OK. [%s]", self._mtx)

    def add_input(self) -> bool:
        """Adds an input"""

    # pylint: disable=R0903
    class Factory:
        """Factory class."""

        __instance: ClassVar[RoutingMatrix | None] = None
        _lock: ClassVar[threading.Lock] = threading.Lock()

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
    """The AudioMixer configuration.

    Attributes:
    """

    _DEFAULT_OUTPUT = "system"

    default_output: str
    conns: set[Connection]
    xputs: set[InputOrOutput]

    def __init__(self):

        self.default_output = self._DEFAULT_OUTPUT
        self.conns = set()
        self.xputs = set()

    @staticmethod
    def get_default() -> Self:
        """Returns a default configuration."""

        result = AudioMixerConfiguration()
        result.default_output = AudioMixerConfiguration._DEFAULT_OUTPUT

        return result

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
        actual_name = Connection.source(name)
        assert any(e.name == actual_name for e in self.xputs)

        result = self.get_xput(actual_name)

        return result

    def get_output(self, name: str) -> Input:
        """Gets an output based on its name from the configuration set."""

        assert name and name.strip()
        actual_name = Connection.sink(name)
        assert any(e.name == actual_name for e in self.xputs)

        result = self.get_xput(actual_name)

        return result

    def add_xput(self, value: InputOrOutput) -> None:
        """Adds an input or ouput object to the configuration set."""

        assert value is not None
        assert value.name and value.name.strip()
        assert not any(e.name == value.name for e in self.xputs), value

        log.debug("Adding object '%s' ...", value.name)

        self.xputs.add(value)

        log.info(
            "Adding object '%s' OK [%s].", value.name, len(self.xputs))

    def remove_xput(self, name: str) -> None:
        """Removes an input or ouput object from the configuration set."""

        assert name and name.strip()
        assert any(e.name == name for e in self.xputs)

        result = next((e for e in self.xputs if e.name == name), None)
        assert result is not None

        log.debug("Removing object '%s' ...", name)

        self.xputs.remove(result)

        log.info("Removing object '%s' OK [%s].", name, len(self.xputs))

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

    _mq: MessageQueue
    _sync_root: threading.Lock
    _callbacks: list[Callable[[threading.Event], None]]
    _state: AudioMixerState
    _routing_matrix: RoutingMatrix
    _cfg: AudioMixerConfiguration
    _mix_bus: Mixbus

    class Event(Enum):
        """Notification events."""

        CONFIGURATION_CHANGING = auto()
        CONFIGURATION_CHANGED = auto()
        DEFAULT_OUTPUT_CHANGED = auto()
        STARTING = auto()
        STARTED = auto()
        STOPPING = auto()
        STOPPED = auto()
        STATE_CHANGED = auto()

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AudioMixer | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

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

    def _on_shutdown(self, message: MessageBase) -> None:
        """Message handler."""

        if not isinstance(message, SystemMessage.Shutdown):
            return

        log.info("on_shutdown: Stopping ...")

        result = self.stop()

        log.info("on_shutdown: Stopping result: %s", result)

    def __init__(self):

        if not AudioMixer.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._sync_root = threading.Lock()
        self._callbacks = []
        self._cfg = None

        # Set private field directly, as not everything is initialised yet.
        self._state = AudioMixerState.STOPPED

        self._routing_matrix = RoutingMatrix.Factory.get()

        self._mq = MessageQueue.Factory.get()
        self._mq.register(
            self._on_shutdown,
            lambda e: isinstance(e, SystemMessage.Shutdown))

        self._mix_bus = Mixbus()

        log.info("Initialising OK.")

    @overload
    def initialise(self) -> bool:
        ...

    @overload
    def initialise(self, cfg: AudioMixerConfiguration) -> bool:
        ...

    def initialise(
            self,
            cfg: AudioMixerConfiguration | None = (
                AudioMixerConfiguration.get_default()
            )
    ) -> bool:
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

        assert cfg is None or isinstance(cfg, AudioMixerConfiguration)

        if cfg is None:
            cfg = AudioMixerConfiguration()

        if self.is_started:
            result = self.stop()
            assert result

        self._mq.publish(msgt.ConfigurationChangingNotification())

        has_default_output_changed = self._cfg is None or (
            self._cfg.default_output != cfg.default_output
        )
        log.debug("%s: Default output: [NEW: %s]",
                  has_default_output_changed,
                  cfg.default_output)
        self._cfg = cfg

        if has_default_output_changed:
            self._mq.publish(
                msgt.DefaultOutputChangedNotification(
                    self._cfg.default_output))

        self._mq.publish(msgt.ConfigurationChangedNotification())

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

    def _set_state(self, value: AudioMixerState) -> None:
        """Private: Sets the private field _state of the audio mixer."""

        self._state = value
        # self.signal(AudioMixer.Event.STATE_CHANGED)

        match value:
            case AudioMixerState.STARTED:
                # self.signal(AudioMixer.Event.STARTED)
                self._mq.publish(
                    msgt.StartedNotification(),
                    msgt.StateChangedNotification())
            case AudioMixerState.STARTING:
                # self.signal(AudioMixer.Event.STARTING)
                self._mq.publish(
                    msgt.StartingNotification(),
                    msgt.StateChangedNotification())
            case AudioMixerState.STOPPING:
                # self.signal(AudioMixer.Event.STOPPING)
                self._mq.publish(
                    msgt.StoppingNotification(),
                    msgt.StateChangedNotification())
            case AudioMixerState.STOPPED:
                # self.signal(AudioMixer.Event.STOPPED)
                self._mq.publish(
                    msgt.StoppedNotification(),
                    msgt.StateChangedNotification())

    def start(self) -> bool:
        """Starts the audio mixer.

        Returns:
            bool: True, if the start command could be initiated; false,
                otherwise. Check `state` for actual state.
        """

        result = False

        log.debug("Starting ...")

        if self._cfg is None:
            log.error("No configuration exists.")
            return result

        if AudioMixerState.STOPPED != self._state:
            return result

        self._set_state(AudioMixerState.STARTING)

        for source in self._cfg.xputs:

            log.debug("Starting '%s' [%s] ...",
                      source.name, type(source).__name__)

            result = source.start()

            if result:
                log.info("Starting '%s' [%s] OK.",
                         source.name, type(source).__name__)
            else:
                log.error("Starting '%s' [%s] FAILED.",
                          source.name, type(source).__name__)

                self._set_state(AudioMixerState.ERROR)
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

            log.info("Connecting '%s' [%s] to '%s' [%s] OK.",
                     conn.this, conn.idx_this, conn.other, conn.idx_other)

        if "system" != self._cfg.default_output:
            self._mix_bus.start()

        clients = JackClient.get()

        # Connect from physical source/capture to bus.
        clt = next(
            (e for e in clients if e.name == Connection.source(
                AudioDevice.LCL.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:LCL-I-DRY-I_1")
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:LCL-I-DRY-I_2")
        clt = next(
            (e for e in clients if e.name == Connection.source(
                AudioDevice.EX1.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:EX1-I-DRY-I_1")
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:EX1-I-DRY-I_2")
        clt = next(
            (e for e in clients if e.name == Connection.source(
                AudioDevice.EX2.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:EX2-I-DRY-I_1")
            JackPort(f"{clt.name}:capture_1").connect_to("MixBus:EX2-I-DRY-I_2")

        # Connect bus to physical sink/playback.
        clt = next(
            (e for e in clients if e.name == Connection.sink(
                AudioDevice.LCL.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort("MixBus:MX0-O_1").connect_to(f"{clt.name}:playback_1")
            JackPort("MixBus:MX0-O_2").connect_to(f"{clt.name}:playback_2")
        clt = next(
            (e for e in clients if e.name == Connection.sink(
                AudioDevice.EX1.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort("MixBus:MX1-O_1").connect_to(f"{clt.name}:playback_1")
            JackPort("MixBus:MX1-O_2").connect_to(f"{clt.name}:playback_2")
        clt = next(
            (e for e in clients if e.name == Connection.sink(
                AudioDevice.EX2.name)), None)
        if isinstance(clt, JackClient):
            log.debug("Connecting ports for '%s' ...", clt.name)
            JackPort("MixBus:MX2-O_1").connect_to(f"{clt.name}:playback_1")
            JackPort("MixBus:MX2-O_2").connect_to(f"{clt.name}:playback_2")

        self._set_state(AudioMixerState.STARTED)
        result = True

        if result:
            log.info("Starting OK.")
        else:
            log.error("Starting FAILED.")

        return result

    def stop(self) -> bool:
        """Stops the audio mixer.

        Returns:
            bool: True, if the stop command could be initiated; false,
                otherwise. Check `state` for actual state.
        """

        result = False

        log.debug("Stopping ...")

        if AudioMixerState.STARTED != self._state:
            return result

        self._set_state(AudioMixer.Event.STOPPING)

        for xput in self._cfg.xputs:

            log.debug("Stopping '%s' [%s] ...", xput.name, type(xput).__name__)

            result = xput.stop()

            if result:
                log.info("Stopping '%s' [%s] OK.",
                         xput.name, type(xput).__name__)
            else:
                log.error("Stopping '%s' [%s] FAILED.",
                          xput.name, type(xput).__name__)

                self._set_state(AudioMixerState.ERROR)
                return False

        self._mix_bus.stop()

        self._set_state(AudioMixerState.STOPPED)
        result = True

        if result:
            log.info("Stopping OK.")
        else:
            log.error("Stopping FAILED.")

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
