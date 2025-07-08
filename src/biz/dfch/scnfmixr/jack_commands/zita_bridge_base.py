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
        args = [self._cmd, "-j", self._name, "-d", self._device, "-c", self._channel_count, "-r", self._sampling_rate]

        log.debug(
            "Creating JACK client '%s' for device '%s' [channel_count: '%s', sampling_rate: '%s'] ...",
            self._name,
            self._device,
            self._channel_count,
            self._sampling_rate
        )

        self._process = Process.start(args, wait_on_completion=False, capture_stdout=False, capture_stderr=True)

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
