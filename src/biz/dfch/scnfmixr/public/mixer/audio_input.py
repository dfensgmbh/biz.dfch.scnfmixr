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

"""Module audio_input."""

from biz.dfch.logging import log

from ...jack_commands import AlsaToJack, JackPort

from ..audio import AlsaInterfaceInfo, Constant
from .audio_input_or_output import AudioInputOrOutput
from .audio_output import AudioOutput
from .input import Input
from .input_or_output import InputOrOutput
from .output import Output

__all__ = [
    "AudioInput",
]


# pylint: disable=R0903
class AudioInput(AudioInputOrOutput, Input):
    """Represents an audio input."""

    def __init__(self, name: str, cfg: AlsaInterfaceInfo):
        super().__init__(
            f"{name}{Constant.JACK_INFIX}{Constant.JACK_INPUT}",
            cfg)

    def start(self) -> bool:

        self._alsa_jack_base = AlsaToJack(
            name=self.name,
            device=f"hw:{self.cfg.card_id},{self.cfg.interface_id}",
            channels=self.cfg.channel_count,
            rate=self.cfg.sample_rate.value)

        return self._alsa_jack_base.is_started

    def stop(self) -> bool:

        self._alsa_jack_base.stop()

        return not self._alsa_jack_base.is_started

    def connect_to(
            self,
            other: InputOrOutput,
            idx_source: int = 0,
            idx_sink: int = 0
    ) -> bool:

        assert other and isinstance(other, Output)
        assert 0 <= idx_source
        assert 0 <= idx_sink

        if isinstance(other, AudioOutput):

            sources = self._alsa_jack_base.get_ports()
            sinks = other._alsa_jack_base.get_ports()

            # Connect from all to all.
            if 0 == idx_source and 0 == idx_sink:

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
            elif 0 == idx_source and 0 != idx_sink:

                result = self._connect_source_all_sink_one(
                    sources,
                    other.name, sinks, idx_sink
                )

            # Connect from specific to all other.
            elif 0 != idx_source and 0 == idx_sink:

                result = self._connect_source_one_sink_all(
                    self.name,
                    sources, idx_source, sinks
                )

            # Connect from specific to specific other.
            elif 0 != idx_source and 0 != idx_sink:

                result = self._connect_source_one_sink_one(
                    self.name,
                    sources, idx_source, other.name, sinks, idx_sink)
            else:
                raise NotImplementedError(type(other))

            return result

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

            log.info("Connecting '%s' to '%s' SUCCEEDED.",
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

            log.info("Connecting '%s' to '%s' SUCCEEDED.",
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

            log.info("Connecting '%s' to '%s' SUCCEEDED.",
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

        log.info("Connecting '%s' to '%s' SUCCEEDED.",
                 source.name, sink.name)

        return True
