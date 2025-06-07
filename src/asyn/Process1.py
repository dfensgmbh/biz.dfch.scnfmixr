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
import asyncio
from collections import deque
import locale
import os
from typing import Optional, Deque, Tuple

__all__ = ["Process1"]


class Process1:

    _STDOUT = "stdout"
    _STDERR = "stderr"

    def __init__(self, process: asyncio.subprocess.Process, encoding: Optional[str] = None) -> None:

        assert process is not None
        self._process = process

        self._encoding = encoding or locale.getpreferredencoding(False)
        self._output_queue: Deque[Tuple[str, str]] = deque()
        self._monitor_task = asyncio.create_task(self._read_output())

    @classmethod
    async def start(
        cls,
        *cmd: list[str],
        cwd: Optional[str] = None,
        wait_on_completion: bool = False,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> Process1:
        """Start an external process and returns a `ProcessInfo` object.
        Args:
            cmd (list[str]): The process to start.
                The program name and its arguments must be passed as a list of strings.
            cwd (str, optional): The working directory for the process.
                If not specified, `os.getcwd()` is used. The path will be asserted if it exists.
            encoding (str, optional): The encoding used for decoding messages from streams.
                If not specified, uses `locale.getpreferredencoding()`
            wait_on_completion (bool, optional): If True, waits for the process to complete before returning.
                Defaults to `False`.
            **kwargs: Additional keyword arguments passed to the underlying process creation logic.
        Returns:
            ProcessInfo: An object containing information about the started process.
        """
        assert cmd is not None

        cwd = cwd or os.getcwd()
        assert os.path.exists(cwd)

        encoding = encoding or locale.getpreferredencoding(False)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
            cwd=cwd,
            **kwargs,
        )

        instance = cls(proc, encoding=encoding)

        if wait_on_completion:
            await proc.wait()

        return instance

    async def _read_output(self) -> None:
        async def read_stream(stream, name):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded_line = line.decode(self._encoding, errors="replace").rstrip()
                self._output_queue.append((name, decoded_line))

        await asyncio.gather(
            read_stream(self._process.stdout, self._STDOUT),
            read_stream(self._process.stderr, self._STDERR),
        )

    def terminate(self, timeout: int = 5) -> None:
        if self._process.returncode is not None:
            return

        self._process.terminate()

    def is_running(self) -> bool:
        return self._process.returncode is None

    def read_stdout(self) -> Optional[str]:
        return self._read_line_in_stream(self._STDOUT)

    def read_stderr(self) -> Optional[str]:
        return self._read_line_in_stream(self._STDERR)

    def read_output(self) -> Optional[str]:
        if self._output_queue:
            _, line = self._output_queue.popleft()
            return line
        return None

    def _read_line_in_stream(self, stream_name: str) -> Optional[str]:
        for idx, (name, line) in enumerate(self._output_queue):
            if name == stream_name:
                del self._output_queue[idx]
                return line
        return None
