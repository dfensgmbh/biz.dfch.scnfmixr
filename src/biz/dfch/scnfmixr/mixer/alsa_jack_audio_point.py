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

"""Module alsa_jack_audio_point."""

from __future__ import annotations
import weakref

from biz.dfch.logging import log

from ..jack_commands import (
    AlsaToJack,
    JackToAlsa,
)
from ..public.mixer import (
    ITerminalSourcePoint,
    ITerminalSourceOrSinkPoint,
    ISignalPath,
    IConnectableSinkPoint,
    IConnectableSourcePoint,
    ITerminalSinkPoint,
    Connection,
)
from ..public.audio import (
    AlsaInterfaceInfo,
    Constant,
)

from .signal_path import SignalPath
from .signal_path_manager import SignalPathManager


__all__ = [
    "AlsaJackAudioPointManager",
    "AlsaJackAudioSourcePoint",
    "AlsaJackAudioSinkPoint",
]


class AlsaJackAudioPointManager():
    """Controls a set of source or sink points of an ALSA JACK bridge."""

    _basename: str
    _source: AlsaInterfaceInfo
    _sink: AlsaInterfaceInfo
    _is_acquired: bool
    _alsa_to_jack_source: AlsaToJack | None
    _jack_to_alsa_sink: JackToAlsa | None

    def __init__(
            self,
            basename: str,
            source: AlsaInterfaceInfo,
            sink: AlsaInterfaceInfo
    ) -> None:

        assert isinstance(basename, str) and basename.strip()
        assert isinstance(source, AlsaInterfaceInfo)
        assert isinstance(sink, AlsaInterfaceInfo)

        self._basename = basename
        self._source = source
        self._sink = sink
        self._is_acquired = False
        self._alsa_to_jack_source = None
        self._jack_to_alsa_sink = None

        self._finalizer = weakref.finalize(self, self.release)

    def __enter__(self) -> tuple[
            list[AlsaJackAudioSourcePoint],
            list[AlsaJackAudioSinkPoint]]:

        return self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def acquire(self) -> tuple[
            list[AlsaJackAudioSourcePoint],
            list[AlsaJackAudioSinkPoint]]:
        """Creates the ALSA JACK bridge."""

        assert not self._is_acquired

        sources: list[AlsaJackAudioSourcePoint] = []
        sinks: list[AlsaJackAudioSinkPoint] = []

        try:

            log.debug("Trying to acquire resource for '%s' ...", self._basename)

            self._alsa_to_jack_source = AlsaToJack(
                name=Connection.jack_alsa_client_source_prefix(
                    self._basename),
                device=Constant.get_raw_device_name(
                    self._source.card_id, self._source.interface_id
                ),
                channels=self._source.channel_count,
                rate=self._source.sample_rate.value)

            self._jack_to_alsa_sink = JackToAlsa(
                name=Connection.jack_alsa_client_sink_prefix(
                    self._basename),
                device=Constant.get_raw_device_name(
                    self._sink.card_id, self._sink.interface_id
                ),
                channels=self._sink.channel_count,
                rate=self._sink.sample_rate.value)

            sources.extend(
                [AlsaJackAudioSourcePoint(e, self)  # pylint: disable=E0110
                 for e in self._alsa_to_jack_source.get_port_names()])

            sinks.extend(
                [AlsaJackAudioSinkPoint(e, self)  # pylint: disable=E0110
                 for e in self._jack_to_alsa_sink.get_port_names()])

            result: tuple[
                list[AlsaJackAudioSourcePoint],
                list[AlsaJackAudioSinkPoint]] = (sources, sinks)

            self._is_acquired = True

            log.info("Trying to acquire resource for '%s' OK.", self._basename)

        except Exception as ex:  # pylint: disable=W0718

            log.error("Trying to acquire resource for '%s' FAILED. [%s]",
                      self._basename, ex, exc_info=True)

        return result

    def release(self):
        """Releases the ALSA JACK bridge."""

        if not self._is_acquired:
            return

        log.debug("Trying to release resources for '%s' ...",
                  self._basename)

        if self._alsa_to_jack_source is not None:
            try:

                log.debug("Releasing resources for '%s' ...",
                          self._alsa_to_jack_source.name)

                name = self._alsa_to_jack_source.name
                self._alsa_to_jack_source.stop()
                self._alsa_to_jack_source = None

                log.info("Releasing resources for '%s' OK.",
                         name)

            except Exception as ex:  # pylint: disable=W0718

                log.error("Trying to release resources for '%s' FAILED. [%s]",
                          self._alsa_to_jack_source.name, ex, exc_info=True)

        if self._jack_to_alsa_sink is not None:
            try:

                log.debug("Releasing resources for '%s' ...",
                          self._jack_to_alsa_sink.name)

                name = self._jack_to_alsa_sink.name
                self._jack_to_alsa_sink.stop()
                self._jack_to_alsa_sink = None

                log.info("Releasing resources for '%s' OK.",
                         name)

            except Exception as ex:  # pylint: disable=W0718

                log.error("Trying to release resources for '%s' FAILED. [%s]",
                          self._jack_to_alsa_sink.name, ex, exc_info=True)

        self._is_acquired = False

        log.info("Trying to release resources for '%s' COMPLETED.",
                 self._basename)

    def connect(
            self,
            source: IConnectableSourcePoint,
            sink: IConnectableSinkPoint
    ) -> ISignalPath:
        """Connects a source point to a sink point."""

        assert isinstance(source, IConnectableSourcePoint)
        assert isinstance(sink, IConnectableSinkPoint)

        mgr = SignalPathManager.Factory.get()
        return SignalPath(source, sink, mgr)  # pylint: disable=E0110

    def is_active(self, point: ITerminalSourceOrSinkPoint) -> bool:
        """Determines whether the signal point is active or not."""

        assert isinstance(point, ITerminalSourceOrSinkPoint)

        if not self._is_acquired:
            return False

        raise NotImplementedError


class AlsaJackAudioSinkPoint(ITerminalSinkPoint):
    """Represents a JACK to ALSA bridge."""

    _ctrl: AlsaJackAudioPointManager

    def __init__(self, name: str, ctrl: AlsaJackAudioPointManager):
        super().__init__(name)

        assert isinstance(ctrl, AlsaJackAudioPointManager)

        self._ctrl = ctrl

    @property
    def is_active(self):
        self._ctrl.is_active(self)

    def connect_to(self, other):
        return self._ctrl.connect(other, self)


class AlsaJackAudioSourcePoint(ITerminalSourcePoint):
    """Represents an ALSA to JACK bridge."""

    _ctrl: AlsaJackAudioPointManager

    def __init__(self, name: str, ctrl: AlsaJackAudioPointManager):
        super().__init__(name)

        assert isinstance(ctrl, AlsaJackAudioPointManager)

        self._ctrl = ctrl

    @property
    def is_active(self):
        self._ctrl.is_active(self)

    def connect_to(self, other):
        return self._ctrl.connect(self, other)
