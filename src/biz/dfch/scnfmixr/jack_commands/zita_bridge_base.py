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

import time

from biz.dfch.logging import log
from biz.dfch.asyn import Process

__all__ = [
    "ZitaBridgeBase",
]


class ZitaBridgeBase:
    """Create a JACK client from an ALSA device."""

    _JACK_CONNECT_FULLNAME = "/bin/jack_connect"
    _SAMPLING_BASERATE = 16000

    def __init__(self, cmd: str, name: str, device: str, channel_count: int, sampling_rate: int):

        assert cmd is not None and "" != cmd.strip()
        assert name is not None and "" != name.strip()
        assert device is not None and "" != device.strip()
        assert 0 < channel_count
        assert 0 == sampling_rate % self._SAMPLING_BASERATE

        self._cmd = cmd
        self._name = name
        self._device = device
        self._channel_count = channel_count
        self._sampling_rate = sampling_rate

        # zita-bridge -j JACK_NAME  -d ALSA_DEVICE -c 2 -r 48000
        # ALSA_DEVICE: hw:CARD=ABC123,DEV=0, hw:CARD=ABC123, hw:1,0, hw:1
        args = [self._cmd, "-j", self._name, "-d", self._device,
                "-c", self._channel_count, "-r", self._sampling_rate]

        log.debug(
            "Creating JACK client '%s' for device '%s' [channel_count: '%s', sampling_rate: '%s'] ...",
            self._name,
            self._device,
            self._channel_count,
            self._sampling_rate
        )

        self._process = Process.start(
            args, wait_on_completion=False, capture_stdout=False, capture_stderr=True)

        assert self._process.is_running
        stderr = self._process.stderr
        assert 0 == len(stderr)

        log.info(
            "Created JACK '%s' for device '%s' with PID [%s] [channel_count: '%s', sampling_rate: '%s'].",
            self._name,
            self._device,
            self._process.pid,
            self._channel_count,
            self._sampling_rate
        )

        # DFTODO - fix timing and the remove this
        time.sleep(3)

    @property
    def process(self) -> Process:
        """Returns process information of the started process."""

        return self._process
