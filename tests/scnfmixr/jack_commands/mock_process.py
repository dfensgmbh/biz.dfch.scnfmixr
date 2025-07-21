# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

"""Module mock_process."""

from __future__ import annotations


class MockProcessJackConnectSucceeds():
    """MockProcess"""

    stderr: list[str] = []

    @staticmethod
    def start(
        args: list[str],
        wait_on_completion: bool = False,
        capture_stdout=False,
        capture_stderr=False,
    ) -> MockProcessJackConnectSucceeds:
        """start"""

        assert isinstance(args, list)
        assert isinstance(wait_on_completion, bool)
        assert isinstance(capture_stdout, bool)
        assert isinstance(capture_stderr, bool)

        return MockProcessJackConnectSucceeds()

    @staticmethod
    def communicate(cmd: list[str],
                    max_wait_time: float = 0,
                    ) -> tuple[list[str],
                               list[str]]:
        """communicate"""
        result: tuple[list[str], list[str]] = ([], [])

        assert isinstance(cmd, list)
        assert isinstance(max_wait_time, (int, float))

        return result


class MockProcessJackConnectFails():
    """MockProcess"""

    stderr: list[str] = [
        "Cannot lock down 107341340 byte memory area (Cannot allocate memory)",
        "cannot connect client, already connected?"
    ]

    @staticmethod
    def start(
        args: list[str],
        wait_on_completion: bool = False,
        capture_stdout=False,
        capture_stderr=False,
    ) -> MockProcessJackConnectFails:
        """start"""

        assert isinstance(args, list)
        assert isinstance(wait_on_completion, bool)
        assert isinstance(capture_stdout, bool)
        assert isinstance(capture_stderr, bool)

        return MockProcessJackConnectFails()

    @staticmethod
    def communicate() -> tuple[list[str], list[str]]:
        """communicate"""
        result: tuple[list[str], list[str]] = ([], [])

        return result


class MockProcessJackDisconnectFails():
    """MockProcess"""

    stderr: list[str] = []

    @staticmethod
    def start(
        args: list[str],
        wait_on_completion: bool = False,
        capture_stdout=False,
        capture_stderr=False,
    ) -> MockProcessJackDisconnectFails:
        """start"""

        assert isinstance(args, list)
        assert isinstance(wait_on_completion, bool)
        assert isinstance(capture_stdout, bool)
        assert isinstance(capture_stderr, bool)

        return MockProcessJackDisconnectFails()

    @staticmethod
    def communicate(cmd: list[str],
                    max_wait_time: float = 0,
                    ) -> tuple[list[str],
                               list[str]]:
        """communicate"""

        assert isinstance(cmd, list)
        assert isinstance(max_wait_time, (int, float))

        stderr: list[str] = [
            ("Cannot lock down 107341340 byte memory"
             "area (Cannot allocate memory)"),
            "cannot disconnect client, already disconnected?"
        ]
        result: tuple[list[str], list[str]] = ([], stderr)

        return result


class MockProcessGetConnections2():
    """MockProcess"""

    @staticmethod
    def communicate(cmd: list[str],
                    max_wait_time: float = 0,
                    ) -> tuple[list[str],
                               list[str]]:
        """communicate"""

        assert isinstance(cmd, list)
        assert isinstance(max_wait_time, (int, float))

        text = """\
system:capture_1
system:capture_2
system:playback_1
system:playback_2
Alsa:LCL-I:capture_1
   Alsa:LCL-O:playback_1
   Alsa:LCL-O:playback_2
   Alsa:EX1-O:playback_1
   Alsa:EX1-O:playback_2
Alsa:LCL-I:capture_2
Alsa:LCL-O:playback_1
   Alsa:LCL-I:capture_1
Alsa:LCL-O:playback_2
   Alsa:LCL-I:capture_1
Alsa:EX1-I:capture_1
Alsa:EX1-I:capture_2
Alsa:EX1-O:playback_1
   Alsa:LCL-I:capture_1
Alsa:EX1-O:playback_2
   Alsa:LCL-I:capture_1
Alsa:EX2-I:capture_1
Alsa:EX2-I:capture_2
Alsa:EX2-O:playback_1
Alsa:EX2-O:playback_2
""".splitlines()

        result: tuple[list[str], list[str]] = (text, [])

        return result


class MockProcessGetConnections3():
    """MockProcess"""

    @staticmethod
    def communicate(cmd: list[str],
                    max_wait_time: float = 0,
                    ) -> tuple[list[str],
                               list[str]]:
        """communicate"""

        assert isinstance(cmd, list)
        assert isinstance(max_wait_time, (int, float))

        text = """\
system:capture_1
        properties: output,physical,terminal,
system:capture_2
        properties: output,physical,terminal,
system:playback_1
        properties: input,physical,terminal,
system:playback_2
        properties: input,physical,terminal,
Alsa:LCL-I:capture_1
   Alsa:LCL-O:playback_1
   Alsa:LCL-O:playback_2
   Alsa:EX1-O:playback_1
   Alsa:EX1-O:playback_2
        properties: output,physical,terminal,
Alsa:LCL-I:capture_2
        properties: output,physical,terminal,
Alsa:LCL-O:playback_1
   Alsa:LCL-I:capture_1
        properties: input,physical,terminal,
Alsa:LCL-O:playback_2
   Alsa:LCL-I:capture_1
        properties: input,physical,terminal,
Alsa:EX1-I:capture_1
        properties: output,physical,terminal,
Alsa:EX1-I:capture_2
        properties: output,physical,terminal,
Alsa:EX1-O:playback_1
   Alsa:LCL-I:capture_1
        properties: input,physical,terminal,
Alsa:EX1-O:playback_2
   Alsa:LCL-I:capture_1
        properties: input,physical,terminal,
Alsa:EX2-I:capture_1
        properties: output,physical,terminal,
Alsa:EX2-I:capture_2
        properties: output,physical,terminal,
Alsa:EX2-O:playback_1
        properties: input,physical,terminal,
Alsa:EX2-O:playback_2
        properties: input,physical,terminal,
""".splitlines()

        result: tuple[list[str], list[str]] = (text, [])

        return result
