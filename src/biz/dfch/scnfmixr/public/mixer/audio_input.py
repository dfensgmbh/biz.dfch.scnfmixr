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

"""Module audio_input."""

from biz.dfch.logging import log

from ...jack_commands import AlsaToJack, JackPort

from ..audio import AlsaInterfaceInfo
from ..audio import Constant

from .audio_input_or_output import AudioInputOrOutput
from .audio_output import AudioOutput
from .connection import Connection
from .input import Input
from .input_or_output import InputOrOutput
from .output import Output

__all__ = [
    "AudioInput",
]


class AudioInput(AudioInputOrOutput, Input):  # pylint: disable=R0903
    """Represents an audio input."""

    def __init__(self, name: str, cfg: AlsaInterfaceInfo):
        super().__init__(
            Connection.source(name),
            cfg)

    def start(self) -> bool:

        self._alsa_jack_base = AlsaToJack(
            name=self.name,
            device=Constant.get_raw_device_name(
                self.cfg.card_id, self.cfg.interface_id
            ),
            channels=self.cfg.channel_count,
            rate=self.cfg.sample_rate.value)

        return self._alsa_jack_base.is_started

    def stop(self) -> bool:

        self._alsa_jack_base.stop()

        return not self._alsa_jack_base.is_started

    def connect_to(
            self,
            other: InputOrOutput,
            idx: int = 0,
            idx_other: int = 0
    ) -> bool:

        assert other and isinstance(other, Output)
        assert 0 <= idx
        assert 0 <= idx_other

        if isinstance(other, AudioOutput):

            sources = self._alsa_jack_base.get_ports()
            sinks = other._alsa_jack_base.get_ports()

            # Connect from all to all.
            if 0 == idx and 0 == idx_other:

                if len(sources) != len(sinks):
                    log.warning("Port count differs. ['%s': %s] [%s: %s]",
                                self.name, len(sources), other.name, len(sinks))

                if 1 == len(sources):

                    result = self._connect_source_one_sink_all(
                        self.name, sources, 1, sinks)

                elif 1 == len(sinks):

                    result = self._connect_source_all_sink_one(
                        sources, other.name, sinks, 1)

                else:
                    result = self._connect_source_all_sink_all(
                        sources, sinks
                    )

            # Connect from all to specific other.
            elif 0 == idx and 0 != idx_other:

                result = self._connect_source_all_sink_one(
                    sources,
                    other.name, sinks, idx_other
                )

            # Connect from specific to all other.
            elif 0 != idx and 0 == idx_other:

                result = self._connect_source_one_sink_all(
                    self.name,
                    sources, idx, sinks
                )

            # Connect from specific to specific other.
            elif 0 != idx and 0 != idx_other:

                result = self._connect_source_one_sink_one(
                    self.name,
                    sources, idx, other.name, sinks, idx_other)
            else:
                raise NotImplementedError(type(other))

            return result

        raise NotImplementedError(
            "Only AudioOutput is currently supported.")

    def _connect_source_all_sink_all(
            self,
            sources: list[JackPort],
            sinks: list[JackPort],
    ) -> bool:
        """Connect from all to all."""

        for source, sink in zip(sources, sinks):

            log.debug("Connecting '%s' to '%s' ...",
                      source.name, sink.name)

            result = source.connect_to(sink.name)

            if not result:
                log.error("Connecting '%s' to '%s' FAILED.",
                          source.name, sink.name)
                return False

            log.info("Connecting '%s' to '%s' OK.",
                     source.name, sink.name)

        return True

    def _connect_source_one_sink_all(
            self,
            source_name: str,
            sources: list[JackPort],
            idx_source: int,
            sinks: list[JackPort],
    ) -> bool:
        """Connect from specific to all other."""
        source = next(
            (
                source
                for source in sources
                if source.is_index(idx_source)
            ),
            None
        )
        if source is None:
            log.warning(
                "Source in '%s' with index '%s' does not exist.",
                source_name, idx_source)
            return False

        for sink in sinks:

            log.debug("Connecting '%s' to '%s' ...",
                      source.name, sink.name)

            result = source.connect_to(sink.name)
            if not result:
                log.error("Connecting '%s' to '%s' FAILED.",
                          source.name, sink.name)
                return False

            log.info("Connecting '%s' to '%s' OK.",
                     source.name, sink.name)

        return True

    def _connect_source_all_sink_one(
            self,
            sources: list[JackPort],
            sink_name: str,
            sinks: list[JackPort],
            idx_sink: int,
    ) -> bool:
        """Connect from all to specific other."""

        sink = next(
            (sink for sink in sinks if sink.is_index(idx_sink)),
            None
        )

        if sink is None:
            log.warning("Sink in '%s' with index '%s' does not exist.",
                        sink_name, idx_sink)
            return False

        for source in sources:

            log.debug("Connecting '%s' to '%s' ...",
                      source.name, sink.name)

            result = source.connect_to(sink.name)
            if not result:
                log.error("Connecting '%s' to '%s' FAILED.",
                          source.name, sink.name)
                return False

            log.info("Connecting '%s' to '%s' OK.",
                     source.name, sink.name)

        return True

    def _connect_source_one_sink_one(
            self,
            source_name: str,
            sources: list[JackPort],
            idx_source: int,
            sink_name: str,
            sinks: list[JackPort],
            idx_sink: int,
    ) -> bool:
        """Connect from specific to specific other."""

        source = next(
            (
                source
                for source in sources
                if source.is_index(idx_sink)
            ),
            None
        )
        if source is None:
            log.warning(
                "Source in '%s' with index '%s' does not exist.",
                source_name, idx_source)
            return False

        sink = next(
            (sink for sink in sinks if sink.is_index(idx_sink)),
            None
        )

        if sink is None:
            log.warning("Sink in '%s' with index '%s' does not exist.",
                        sink_name, idx_sink)
            return False

        log.debug("Connecting '%s' to '%s' ...",
                  source.name, sink.name)

        result = source.connect_to(sink.name)

        if not result:
            log.error("Connecting '%s' to '%s' FAILED.",
                      source.name, sink.name)
            return False

        log.info("Connecting '%s' to '%s' OK.",
                 source.name, sink.name)

        return True

    def invoke(self):
        raise NotImplementedError
