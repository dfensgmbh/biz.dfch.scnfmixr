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

"""Module jack_transport."""

from biz.dfch.asyn import Process
from biz.dfch.logging import log


class JackTransport:
    """Starts or stops JACK transport control."""

    _SIGTERM_MESSAGE = "signal received, exiting ..."
    _JACK_TRANSPORT_FULLNAME = "/bin/jack_transport"
    _JACK_TRANSPORT_CMD_LOCATE_POS0 = "locate 0"
    _JACK_TRANSPORT_CMD_START = "play"
    _JACK_TRANSPORT_CMD_STOP = "stop"
    _JACK_TRANSPORT_CMD_EXIT = "exit"

    def _is_stderr_ok(self, value: list[str]) -> bool:
        if value is None or not value:
            return True
        if len(value) == 1 and value[0].startswith(self._SIGTERM_MESSAGE):
            return True
        return False

    def start(self) -> None:
        """Starts JACK transport control."""

        log.debug("Starting ...")

        cmd: list[str] = [
            JackTransport._JACK_TRANSPORT_FULLNAME,
        ]
        stdin: list[str] = [
            JackTransport._JACK_TRANSPORT_CMD_LOCATE_POS0,
            JackTransport._JACK_TRANSPORT_CMD_START,
            JackTransport._JACK_TRANSPORT_CMD_EXIT,
        ]

        _, stderr = Process.communicate(cmd, stdin)

        if self._is_stderr_ok(stderr):
            log.info("Starting OK.")
        else:
            log.warning("Starting returned with error. [%s]", stderr)

    def stop(self) -> None:
        """Starts JACK transport control."""

        log.debug("Stopping ...")

        cmd: list[str] = [
            JackTransport._JACK_TRANSPORT_FULLNAME,
        ]

        stdin: list[str] = [
            JackTransport._JACK_TRANSPORT_CMD_STOP,
            JackTransport._JACK_TRANSPORT_CMD_EXIT,
        ]

        _, stderr = Process.communicate(cmd, stdin)

        if self._is_stderr_ok(stderr):
            log.info("Stopping OK.")
        else:
            log.warning("Stopping returned with error. [%s]", stderr)
