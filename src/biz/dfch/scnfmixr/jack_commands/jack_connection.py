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

"""Module for handling JACK commands."""

from __future__ import annotations
import os
import time

from biz.dfch.logging import log
from biz.dfch.asyn import Process

from text import MultiLineTextParser
from text import MultiLineTextParserContext

__all__ = [
    "JackConnection",
]


class JackConnection:
    """Create a JACK connection between a `source` and a `sink`."""

    _JACK_CONNECT_FULLNAME = "/bin/jack_connect"
    _JACK_LSP_FULLNAME = "/bin/jack_lsp"
    _JACK_LSP_OPTION_CONNECTIONS = "-c"
    _JACK_LSP_CLIENT_PORT_SEPARATOR = ':'

    class Factory:
        """Factory class for creating `JackConnection` instances."""

        @staticmethod
        def create(source: str, sink: str) -> JackConnection | None:
            """Creates a `JackConnection` instance.

            Args:
                source (str): The name of the JACK client to connect from.
                sink (str): The name of the JACK client to connect to.

            Returns:
                JackConnection: If successful, the created connection, or `None`
                otherwise.
            """

            assert source and source.strip()
            assert sink and sink.strip()

            try:

                return JackConnection(source, sink)

            except RuntimeError:

                return None

    # DFTODO - is this method inside the correct class?
    @staticmethod
    def has_client_name(name: str) -> bool:
        """Determines whether a JACK client names exists."""

        assert name and name.strip()

        cmd: list[str] = [
            JackConnection._JACK_LSP_FULLNAME
        ]

        text, _ = Process.communicate(cmd, max_wait_time=0.25)

        return any(e for e in text if e.split(
            JackConnection._JACK_LSP_CLIENT_PORT_SEPARATOR)[0] == name)

    # DFTODO - is this method inside the correct class?
    @staticmethod
    def get_client_names() -> list[str]:
        """Gets JACK client names."""

        cmd: list[str] = [
            JackConnection._JACK_LSP_FULLNAME
        ]

        text, _ = Process.communicate(cmd, max_wait_time=0.25)

        return list({
            e.split(JackConnection._JACK_LSP_CLIENT_PORT_SEPARATOR, 1)[0]
            for e in text})

    @staticmethod
    def get_ports(name: str) -> list[str]:
        """Show JACK ports for the specified JACK name.

        Args:
            name (str): The channel independent name of the jack sink to
                connect to.

        Returns:
            list[str]: A list of port names.
        """

        assert name and name.strip()

        result: list[str] = []

        cmd: list[str] = []
        cmd.append(JackConnection._JACK_LSP_FULLNAME)
        cmd.append(name)

        text, _ = Process.communicate(cmd, max_wait_time=0.25)

        visitor = JackConnection.PortVisitor()
        dic = {
            name: visitor.process_port,
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=3,
            dic=dic)
        parser.parse(text)

        result = visitor.items

        return result

    @staticmethod
    def get_connections(name: str) -> list[str]:
        """Show JACK connections for the specified JACK name.

        Args:
            name (str): The channel independent name of the jack sink to
                connect to.

        Returns:
            list[str]: A list of clients connected to `name`.
        """

        assert name and name.strip()

        result: list[str] = []

        cmd: list[str] = []
        cmd.append(JackConnection._JACK_LSP_FULLNAME)
        cmd.append(name)
        cmd.append(JackConnection._JACK_LSP_OPTION_CONNECTIONS)

        text, _ = Process.communicate(cmd)

        visitor = JackConnection.ConnectionVisitor()
        dic = {
            f"{name}": visitor.process_port,
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=3,
            dic=dic,
            default=visitor.process_connection)
        parser.parse(text, is_regex=False)

        result = visitor.items

        return result

    def __init__(self, source: str, sink: str) -> None:
        """Initialise an instance of this class.

        Args:
            source (str): The JACK source to connect to.
            sink (str): The JACK sink to connecto to.
        """

        assert source and source.strip()
        assert sink and sink.strip()

        self._source = source
        self._sink = sink

        args = [self._JACK_CONNECT_FULLNAME, self._source, self._sink]

        log.debug("Connecting '%s' to '%s' ...", source, sink)

        self._process = Process.start(args,
                                      wait_on_completion=False,
                                      capture_stdout=True,
                                      capture_stderr=True)

        stderr = self._process.stderr
        if 0 == len(stderr):

            self._is_active = True
            time.sleep(1)

            log.info("Connecting '%s' to '%s' completed.", source, sink)

            return

        message = f"Connecting '{source}' to '{sink}' FAILED."
        log.error(message)
        log.error(os.sep.join(stderr))

        raise RuntimeError(message)

    class ConnectionVisitor:
        """A visitor for parsing `jack_lsp` connection output."""

        def __init__(self):
            """Returns an instance of this object."""

            self.is_section_active = False
            self.has_section_processed = False
            self.items = []

        def process_port(self, ctx: MultiLineTextParserContext) -> bool:
            """Process the specified port.

            Args:
                ctx (MultiLineTextParserContext): The parser context.

            Returns:
                bool: True, if processing should continue; false otherwise.
            """

            assert ctx

            if 0 != ctx.level:
                return True

            self.is_section_active = True
            return True

        def process_connection(self, ctx: MultiLineTextParserContext) -> bool:
            """Process any other line.

            Args:
                ctx (MultiLineTextParserContext): The parser context.

            Returns:
                bool: True, if processing should continue; false otherwise.
            """

            assert ctx

            if not self.is_section_active:
                return True

            # Stop processing after port section.
            if 0 == ctx.level:
                self.is_section_active = False
                self.has_section_processed = True
                return False

            if 1 != ctx.level:
                return True

            self.items.append(ctx.text)
            return True

    class PortVisitor:
        """A visitor for parsing `jack_lsp` port output."""

        def __init__(self):
            """Returns an instance of this object."""

            self.items = []

        def process_port(self, ctx: MultiLineTextParserContext) -> bool:
            """Process the specified port.

            Args:
                ctx (MultiLineTextParserContext): The parser context.

            Returns:
                bool: True, if processing should continue; false otherwise.
            """

            assert ctx

            if 0 != ctx.level:
                return False

            self.items.append(ctx.text)
            return True
