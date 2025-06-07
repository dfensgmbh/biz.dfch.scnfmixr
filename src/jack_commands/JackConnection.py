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

from __future__ import annotations
import os

from asyn import Process
from log import log

__all__ = [
    "JackConnection",
]


class JackConnection:
    """Create a JACK connection between a `source` and a `sink`."""

    class Factory:
        """Factory class for creating `JackConnection` instances."""

        def create(source: str, sink: str) -> JackConnection | None:
            """Creates a `JackConnection` instance.
            Args:
                source (str): The name of the JACK client to connect from.
                sink (str): The name of the JACK client to connect to.
            Returns:
                JackConnection: The created connection if successful, or `None` otherwise.
            """

            assert source is not None and "" != source.strip()
            assert sink is not None and "" != sink.strip()

            try:
                return JackConnection(source, sink)
            except RuntimeError:
                return None

    _JACK_CONNECT_FULLNAME = "/bin/jack_connect"

    def __init__(self, source: str, sink: str):

        assert source is not None and "" != source.strip()
        assert sink is not None and "" != sink.strip()

        self._is_active = False
        self._source = source
        self._sink = sink

        args = [self._JACK_CONNECT_FULLNAME, self._source, self._sink]

        log.debug(f"Connecting '{source}' to '{sink}' ...")

        self._process = Process.start(args, wait_on_completion=True, capture_stdout=True, capture_stderr=True)
        # self._process = Process.Factory.create(args, wait_on_completion=True, capture_stdout=True, capture_stderr=True)

        stderr = self._process.stderr
        if 0 == len(stderr):

            self._is_active = True
            log.info(f"Connecting '{source}' to '{sink}' completed.")

            return

        message = f"Connecting '{source}' to '{sink}' FAILED."
        log.error(message)
        log.error(os.sep.join(stderr))

        raise RuntimeError(message)

    @property
    def is_active(self) -> bool:
        """`True` if the connection is active. `False` otherwise."""

        return self._is_active

    def disconnect(self) -> bool:
        """Disconnects an active JACK connection.
        Returns:
            bool: `True` if the connection was active. `False` otherwise.
        """

        if not self._is_active:
            return False

        # DFTODO - disconnect existing connection.
        # self._has_connection = False
        pass
