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

"""Module for starting and managing processes."""

from __future__ import annotations

import locale
import os
import subprocess
import threading
import time
from typing import IO, Optional, Sequence, Tuple

from biz.dfch.logging import log
from col import CircularQueue

__all__ = ["Process"]


class Process:
    """Starts and stops processes. Use `start()` to initialise this class."""

    _MAX_QUEUE_SIZE = 4096

    _TUPLE_KEY_INDEX = 0
    _TUPLE_KEY_VALUE = 1

    _STDOUT = "stdout"
    _STDERR = "stderr"

    def __init__(self, popen: subprocess.Popen, encoding: str) -> None:
        """Initialise a `Process` instance. Use `start` to initialise this
        class. Should not be called directly.

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

        self._queue = CircularQueue[Tuple[str, str]](self._MAX_QUEUE_SIZE)

    @property
    def pid(self) -> int:
        """Returns the PID of the process.

        Args:
            None:

        Returns:
            int: The PID of the process.
        """

        assert self._popen

        return self._popen.pid

    @property
    def is_running(self) -> bool:
        """Determines wether the process is still running.

        Args:
            None:

        Returns:
            bool: True if running; false otherwise.
        """

        return self._popen.poll() is None

    @property
    def exit_code(self) -> int | None:
        """Returns the numeric exit code if the process has stopped.

        Args:
            None:

        Returns:
            int: The exit code or `None` if the process is still running.
        """
        return self._popen.poll()

    def stop(self, max_wait_time: int = 5, force: bool = False) -> bool:
        """Stops a running process, then forcibly terminates if specified and
        if it is still running. Does nothing if the process is already stopped.

        Args:
            max_wait_time (int): Maximum number of seconds to wait for graceful
                termination.
            force (bool): If `True`, the process is forcibly stopped. `False`
                by default.

        Returns:
            bool: Returns `True` if the process could be stopped; `False` if
            the process was already stopped.

        Raises:
            RuntimeError: If the process could not be stopped.
        """

        assert 0 <= max_wait_time

        try:

            if self._popen.stdin:
                self._popen.stdin.flush()

            if self._popen.stdout:
                self._popen.stdout.flush()

            if self._popen.stderr:
                self._popen.stderr.flush()

            # Process already stopped.
            if self._popen.poll() is not None:
                return False

            self._popen.terminate()

            end_time = time.monotonic() + max_wait_time
            while end_time > time.monotonic():
                if self._popen.poll() is not None:
                    return True

                time.sleep(0.25)

            # Process stopped gracefully.
            if self._popen.poll() is not None:
                return True

            if not force:

                message = f"Process [{self._popen.pid}] could not be stopped" \
                    "gracefully."
                log.error(message, exc_info=True)

                raise RuntimeError(message)

            self._popen.kill()

            start_time = time.time_ns()
            while time.time_ns() - start_time < max_wait_time * 10**9:
                if self._popen.poll() is not None:
                    return True

                time.sleep(0.25)

            # Process stopped forcibly.
            return self._popen.poll() is not None

        except Exception as ex:

            message = f"Process [{self._popen.pid}] could not be stopped."
            log.error(message, exc_info=True)
            raise RuntimeError(message) from ex

    @classmethod
    def start(
        cls,
        cmd: list[str],
        wait_on_completion: bool = False,
        capture_stdout: bool = False,
        capture_stderr: bool = False,
        cwd: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> Process:
        """Starts a specified process and optionally waits until its completion.

        Args:
            cmd (list[str]): The process with its arguments to be started.
            cmd (str, optional): The working directory of the process to be
                started. If no working directory is given, the current working
                directory of the calling process is used.
            encoding (str, optional): The charset to be used for the process to
                be started. If no encoding is given,
                the current encoding of the calling process is used.

        Returns:
            Process: An instance of `Process` containing information about the
            process started.
        """

        assert cmd is not None and 0 < len(cmd)
        args = [str(arg) for arg in cmd]

        cwd = cwd or os.getcwd()
        assert os.path.exists(cwd)

        encoding = encoding or locale.getpreferredencoding(False)

        log.debug("Trying to start process... [%s]", args)
        # pylint: disable=consider-using-with
        result = subprocess.Popen(
            args=args,
            cwd=cwd,
            encoding=encoding,
            text=True,
            bufsize=1,
            stdout=subprocess.PIPE if capture_stdout else subprocess.DEVNULL,
            stderr=subprocess.PIPE if capture_stderr else subprocess.DEVNULL,
            **kwargs,
        )

        log.debug("Started process '%s' [%s].", args[0], result.pid)

        process = cls(result, encoding)

        if capture_stdout:
            process._stdout_thread = threading.Thread(
                target=process._read_stream, args=(
                    process._popen.stdout, process._STDOUT)
            )
            log.debug(
                "Starting reading from pipe '%s' [%s] ...", process._STDOUT, result.pid)
            process._stdout_thread.start()

        if capture_stderr:
            process._stderr_thread = threading.Thread(
                target=process._read_stream, args=(
                    process._popen.stderr, process._STDERR)
            )
            log.debug(
                "Starting reading from pipe '%s' [%s] ...", process._STDERR, result.pid)
            process._stderr_thread.start()

        if not wait_on_completion:
            return process

        while process.is_running:
            time.sleep(1)

        return process

    def _read_stream(self, stream: IO[str], name: str) -> None:
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

                value = line.rstrip(os.linesep)
                self._queue.enqueue((name, value))

                # if stream.closed:
                #     return

        except Exception as ex:  # pylint: disable=broad-exception-caught
            log.warning("Error reading from stream '%s' [%s]. %s",
                        name,
                        self._popen.pid,
                        ex)

    @property
    def stdout(self) -> Sequence[str]:
        """Returns all `STDOUT` messages from the started process, if `start`
        was called with `capture_stdout`.

        Returns:
            Sequence[str]: A sequence containing all output that was sent to
            `STDOUT` by the process.
        """

        items = self._queue.dequeue_filter(
            lambda e: e[self._TUPLE_KEY_INDEX] == self._STDOUT)
        result = [item[self._TUPLE_KEY_VALUE] for item in items]

        return result

    @property
    def stderr(self) -> Sequence[str]:
        """Returns all `STDERR` messages from the started process, if `start`
        was called with `capture_stderr`.

        Returns:
            Sequence[str]: A sequence containing all output that was sent to
            `STDERR` by the process.
        """

        items = self._queue.dequeue_filter(
            lambda e: e[self._TUPLE_KEY_INDEX] == self._STDERR)
        result = [item[self._TUPLE_KEY_VALUE] for item in items]

        return result

    @property
    def output(self) -> Sequence[str]:
        """Returns all output (`STDOUT` and `STDERR`) messages from the started
        process, if `start` was called with  `capture_stdout` and/or
        `capture_stderr`.

        Returns:
            Sequence[str]: A sequence containing all output that was sent to
            `STDERR` by the process.
        """

        items = self._queue.dequeue_filter(lambda _: True)
        result = [item[self._TUPLE_KEY_VALUE] for item in items]

        return result
