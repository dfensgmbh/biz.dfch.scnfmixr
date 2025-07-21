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

"""Module jack_connection."""

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
    _JACK_DISCONNECT_FULLNAME = "/usr/bin/jack_disconnect"
    _JACK_LSP_FULLNAME = "/bin/jack_lsp"
    _JACK_LSP_OPTION_CONNECTIONS = "-c"
    _JACK_LSP_OPTION_PORTS = "-p"
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

    @staticmethod
    def get_connections2() -> dict[str, list[str]]:
        """Gets connnections."""

        cmd: list[str] = [
            JackConnection._JACK_LSP_FULLNAME,
            JackConnection._JACK_LSP_OPTION_CONNECTIONS,
        ]

        text, _ = Process.communicate(cmd)

        visitor = JackConnection.ConnectionVisitor2()

        parser = MultiLineTextParser(
            indent=" ",
            length=3,
            dic={},
            default=visitor.process_default)
        parser.parse(text, is_regex=False)

        return visitor.result

    @staticmethod
    def get_connections3() -> dict[tuple[str, bool], list[str]]:
        """Gets connnections with source and sink information.
        
        Returns:
            dict (tuple[str, bool], list[str])
        """

        cmd: list[str] = [
            JackConnection._JACK_LSP_FULLNAME,
            JackConnection._JACK_LSP_OPTION_CONNECTIONS,
            JackConnection._JACK_LSP_OPTION_PORTS,
        ]

        text, _ = Process.communicate(cmd)

        visitor = JackConnection.ConnectionVisitor3()

        dic = {
            "properties: input,": visitor.process_properties_input,
            "properties: output,": visitor.process_properties_output,
        }
        parser = MultiLineTextParser(
            indent=" ",
            length=1,
            dic=dic,
            default=visitor.process_default)
        parser.parse(text, is_regex=False)

        return visitor.result

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

    def disconnect(self) -> bool:
        """Disconnect a JACK connection."""

        cmd: list[str] = [
            self._JACK_DISCONNECT_FULLNAME,
            self._source,
            self._sink,
        ]

        # msg = "cannot connect client, already connected?"
        msg = "cannot disconnect client, already disconnected?"

        _, text = Process.communicate(cmd, max_wait_time=0.25)

        return msg not in text

    def is_connected(self) -> bool:
        """Determines whether a connection exists of not."""
        return JackConnection.check_connection(self._source, self._sink)

    @staticmethod
    def check_connection(source: str, sink: str) -> bool:
        """Determines whether a connection exists of not."""

        assert isinstance(source, str) and source.strip()
        assert isinstance(sink, str) and sink.strip()

        cmd: list[str] = [
            JackConnection._JACK_LSP_FULLNAME,
            JackConnection._JACK_LSP_OPTION_CONNECTIONS,
        ]

        text, _ = Process.communicate(cmd, max_wait_time=0.25)

        return list({
            e.split(JackConnection._JACK_LSP_CLIENT_PORT_SEPARATOR, 1)[0]
            for e in text})

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

    class ConnectionVisitor2:
        """A visitor for parsing `jack_lsp` connection output."""

        current_key: str
        result: dict[str, list[str]]

        def __init__(self):
            """Returns an instance of this object."""

            self.current_key = ""
            self.result = {}

        def process_default(self, ctx: MultiLineTextParserContext) -> bool:
            """Process any line."""

            assert ctx
            assert ctx.level in [0, 1], ctx.level

            if 0 == ctx.level:
                if ctx.text not in self.result:
                    self.result[ctx.text] = []
                    self.current_key = ctx.text

                return True

            if 1 == ctx.level:
                self.result[self.current_key].append(ctx.text)

                return True

    class ConnectionVisitor3:
        """A visitor for parsing `jack_lsp` connection output."""

        current_key: str
        is_sink: bool
        connections: list[str]
        result: dict[str, list[str]]

        def __init__(self):
            """Returns an instance of this object."""

            self.current_key = ""
            self.is_sink = False
            self.connections = []
            self.result = {}

        def process_properties_input(
                self,
                _: MultiLineTextParserContext) -> bool:
            """Process input."""

            # 'input' is sink, which is an "output", contraire ...
            self.is_sink = True
            key = (self.current_key, self.is_sink)
            self.result[key] = []
            self.result[key].extend(self.connections)

            return True

        def process_properties_output(
                self,
                _: MultiLineTextParserContext) -> bool:
            """Process output."""

            # 'output' is source, which is an "input", contraire ...
            self.is_sink = False
            key = (self.current_key, self.is_sink)
            self.result[key] = []
            self.result[key].extend(self.connections)

            return True

        def process_default(self, ctx: MultiLineTextParserContext) -> bool:
            """Process any line."""

            assert ctx
            assert ctx.level in range(0, 9), ctx.level

            if 0 == ctx.level:
                if ctx.text not in self.result:
                    self.connections = []
                    self.current_key = ctx.text
                    self.is_sink = False

                return True

            if 3 == ctx.level:
                self.connections.append(ctx.text)

                return True
