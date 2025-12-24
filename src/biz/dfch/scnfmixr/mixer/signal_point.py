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

"""Module signal_point."""

from __future__ import annotations
from typing import cast

from biz.dfch.logging import log

import biz.dfch.scnfmixr.public.mixer.iterminal_device as pt
import biz.dfch.scnfmixr.public.mixer.iconnectable_point_or_set
import biz.dfch.scnfmixr.public.mixer.iconnectable_point
import biz.dfch.scnfmixr.public.mixer.iconnectable_sink
import biz.dfch.scnfmixr.public.mixer.iconnectable_set
import biz.dfch.scnfmixr.public.mixer.isignal_path
import biz.dfch.scnfmixr.public.mixer.iterminal_source_or_sink_point

from ..jack_commands import AlsaToJack, JackToAlsa

from ..alsa_usb import (
    AlsaStreamInfoParser,
)
from ..public.mixer import ConnectionInfo
from ..public.audio import (
    AlsaInterfaceInfo,
    Format,
    SampleRate,
    Constant,
)

from .alsa_jack_audio_point import AlsaJackAudioPointManager


__all__ = [
    "BestAlsaJackAudioDevice",
]


class BestAlsaJackAudioDevice(pt.ITerminalDevice):  # pylint: disable=R0901
    """Represents an ALSA audio device."""

    _PROC_ASOUND_PATH_TEMPLATE = "/dev/proc/asound/card%s"

    _display_name: str
    _card_id: int
    _device_id: int
    _ctrl: AlsaJackAudioPointManager

    def __init__(
            self,
            display_name: str,
            card_id: int,
            device_id: int = 0,
            parser: AlsaStreamInfoParser | None = None,
    ):
        """Initialises a new ALSA to JACK audio bridge."""

        super().__init__(Constant.get_raw_device_name(card_id, device_id))

        assert isinstance(display_name, str) and display_name.strip()
        assert isinstance(card_id, int) and 0 <= card_id
        assert isinstance(device_id, int) and 0 <= device_id
        assert 0 == device_id, "Currently, only 0 == device_id is implemented."
        assert parser is None or isinstance(parser, AlsaStreamInfoParser)

        self._display_name = display_name
        self._card_id = card_id
        self._device_id = device_id

        if parser is None:
            parser = AlsaStreamInfoParser(self._card_id)

        capture_interface = parser.get_best_capture_interface()
        log.debug(capture_interface)

        source = AlsaInterfaceInfo(
            card_id=self._card_id,
            interface_id=parser.interface_id,
            channel_count=capture_interface.channel_count,
            format=Format(capture_interface.format),
            bit_depth=Format(capture_interface.format).get_bit_depth(),
            sample_rate=SampleRate(capture_interface.get_best_rate()),
        )

        playback_interface = parser.get_best_playback_interface()
        log.debug(playback_interface)

        sink = AlsaInterfaceInfo(
            card_id=self._card_id,
            interface_id=parser.interface_id,
            channel_count=playback_interface.channel_count,
            format=Format(playback_interface.format),
            sample_rate=SampleRate(playback_interface.get_best_rate()),
            bit_depth=Format(playback_interface.format).get_bit_depth(),
        )

        self._ctrl = AlsaJackAudioPointManager(
            self._display_name, source, sink)

        sources, sinks = self._ctrl.acquire()

        assert sources and isinstance(sources, list)
        assert sinks and isinstance(sinks, list)

        self._items.extend(sources)
        self._items.extend(sinks)

    @property
    def card_id(self) -> int:
        """Returns the ALSA card id."""
        return self._card_id

    @property
    def device_id(self) -> int:
        """Returns the ALSA device id."""
        return self._device_id

    def connect_to(
            self,
            other: biz.dfch.scnfmixr.public.mixer.iconnectable_point_or_set.IConnectablePointOrSet
    ) -> set[biz.dfch.scnfmixr.public.mixer.isignal_path.ISignalPath]:

        assert isinstance(
            other, biz.dfch.scnfmixr.public.mixer.iconnectable_point_or_set.IConnectablePointOrSet)

        result: list[biz.dfch.scnfmixr.public.mixer.isignal_path.ISignalPath] = []

        # Is other source or sink?
        if isinstance(other, biz.dfch.scnfmixr.public.mixer.iconnectable_sink.IConnectableSink):
            these = self.sources
        else:
            these = self.sinks

        # Case A: other is point
        # Connect _all_ items to the point.
        if isinstance(other, biz.dfch.scnfmixr.public.mixer.iconnectable_point.IConnectablePoint):
            for this in these:
                result.append(this.connect_to(other))
            return result

        # Case B: other is set.
        others = cast(
            biz.dfch.scnfmixr.public.mixer.iconnectable_set.IConnectableSet, other)

        # Case B1: source.channel_count == sink.channel_count
        # Connect all source channels to sink channels, 1 : 1
        if len(these) == len(others.points):
            for i, this in enumerate(these):
                result.append(this.connect_to(others[i]))
            return result

        # Case B3: these.channel_count > others.channel_count
        # Only connect up to the number of others.channel_count.
        if len(these) > len(others):
            for i in range(0, len(others)):  # pylint: disable=C0200
                result.append(these[i].connect_to(others[i]))
            return result

        # Case B2: source.channel_count < sink.channel_count

        # Case B2.1: source.channel_count == 1 &&  < sink.channel_count
        # Connect source channel to all destination channels.
        if 1 == len(these):
            for i in range(0, len(others)):  # pylint: disable=C0200
                result.append(these[0].connect_to(others[i]))
            return result

        # Case B2.2: source.channel_count != 1 &&  < sink.channel_count
        # Only connect up to the number of source.channel_count.
        for i, this in enumerate(these):
            result.append(this.connect_to(others[i]))
        return result

    @property
    def points(self) -> list[biz.dfch.scnfmixr.public.mixer.iterminal_source_or_sink_point.ITerminalSourceOrSinkPoint]:
        return self._items

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError
