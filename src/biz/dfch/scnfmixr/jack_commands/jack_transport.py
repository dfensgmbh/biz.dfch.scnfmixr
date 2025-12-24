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
