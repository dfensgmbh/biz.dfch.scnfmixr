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
from collections import deque
import locale
import os
import subprocess
import threading
import time
from typing import Deque, IO, Optional, Tuple

from log import log

__all__ = ["Process"]


class Process:
    """Starts and stops processes. Use `start()` to initialise this class."""

    _STDOUT = "stdout"
    _STDERR = "stderr"

    def __init__(self, popen: subprocess.Popen, encoding: str) -> None:
        """Initialise a process instance. Use `start()` to initialise this class.
        Args:
            process (subprocess.Popen): An instance of `Popen`.
            encoding (str): The charset to used for the process started.
        Returns:
            Process: An instance of this class.
        """

        assert popen is not None
        self._popen = popen

        assert encoding is not None and "" != encoding.strip()
        self._encoding = encoding or locale.getpreferredencoding(False)

        self._output_queue: Deque[Tuple[str, str]] = deque()

        # self._stdout_thread = threading.Thread(target=self.read_stream, args=(self._popen.stdout, self._STDOUT))
        # self._stderr_thread = threading.Thread(target=self.read_stream, args=(self._popen.stderr, self._STDERR))
        # print(f"Starting thread '{self._STDOUT}' ...")
        # self._stdout_thread.start()
        # print(f"Starting thread '{self._STDERR}' ...")
        # self._stderr_thread.start()

    @property
    def is_running(self) -> bool:
        """Returns `True` if the process is still running. Returns `False` if the process has stopped."""
        return self._popen.poll() is None

    @property
    def exit_code(self) -> int | None:
        """Returns the numeric exit code if the process has stopped. Returns `None` if the process is still running."""
        return self._popen.poll()

    def stop(self, force: bool = False) -> bool:
        """Stops a running process. Does nothing if the process is already stopped.
        Args:
            force (bool): If `True`, the process is forcibly stopped. `False` by default.
        Returns:
            bool: Returns `True` if the process could be stopped. `False` if the process was already stopped.
        """
        pass

    @classmethod
    def start(
        cls,
        cmd: list[str],
        wait_on_completion: bool = False,
        redirect_stdout: bool = False,
        redirect_stderr: bool = False,
        cwd: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> Process:
        """Starts a specified process and optionally waits until its completion.
        Args:
            cmd (list[str]): The process with its arguments to be started.
            cmd (str, optional): The working directory of the process to be started. If no working directory is given,
                the current working directory of the calling process is used.
            encoding (str, optional): The charset to be used for the process to be started. If no encoding is given,
                the current encoding of the calling process is used.
        Returns:
            Process: An instance of `Process` containing information about the process started.
        """

        assert cmd is not None and 0 < len(cmd)
        args = tuple(cmd)

        cwd = cwd or os.getcwd()
        assert os.path.exists(cwd)

        encoding = encoding or locale.getpreferredencoding(False)

        result = subprocess.Popen(
            args=args,
            cwd=cwd,
            encoding=encoding,
            text=True,
            bufsize=1,
            stdout=subprocess.PIPE if redirect_stdout else None,
            stderr=subprocess.PIPE if redirect_stderr else None,
            **kwargs,
        )

        log.debug(f"Started process '{args[0]}' [{result.pid}].")

        process = Process(result, encoding)

        if redirect_stdout:
            process._stdout_thread = threading.Thread(
                target=process.read_stream, args=(process._popen.stdout, process._STDOUT)
            )
            log.debug(f"Starting reading from pipe '{process._STDOUT}' [{result.pid}] ...")
            process._stdout_thread.start()

        if redirect_stderr:
            process._stderr_thread = threading.Thread(
                target=process.read_stream, args=(process._popen.stderr, process._STDERR)
            )
            log.debug(f"Starting reading from pipe '{process._STDERR}' [{result.pid}] ...")
            process._stderr_thread.start()

        if not wait_on_completion:
            return process

        while process.is_running:
            time.sleep(1)

        return process

    def read_stream(self, stream: IO[str], name: str) -> None:
        """Reads data from a specified pipe.
        Args:
            pipe (IO[str]): The pipe to read from.
            name (str): The display name of the stream.
        Returns:
            None: The method does not return anything.
        """

        assert stream is not None
        assert name is not None and "" != name.strip()

        try:
            for line in iter(stream.readline, ""):

                print(f"{name}: {line.rstrip(os.linesep)}")

        except Exception as ex:
            log.warning(f"Error reading from stream '{name}' [{self._popen.pid}]. {ex}")
