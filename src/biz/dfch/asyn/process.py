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

"""Module for starting and managing processes."""

from __future__ import annotations

import locale
import os
import subprocess
import threading
import time
import signal
from typing import IO, Sequence, Tuple

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

    _stdout_thread: threading.Thread
    _stderr_thread: threading.Thread

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
        assert encoding is not None and "" != encoding.strip()

        self._stdout_thread = None
        self._stderr_thread = None

        self._popen = popen
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
            force (bool): If `True`, the process is forcibly stopped; false
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

    @staticmethod
    def communicate(
        cmd: list[str],
        stdin: list[str] | None = None,
        cwd: str = None,
        max_wait_time: float = 5,
        encoding: str = "utf-8",
        env: dict[str, str] = {},
        **kwargs
    ) -> tuple[list[str], list[str]]:
        """Sends text to a process and waits for return synchronously.

        Args:
            cmd (list[str]): The command to execute with its arguments.
            stind (list[str] | None): The input to be sent to stdin of the
                process as list of strings or `None` (default)). For every item
                in `stdin` a single line of text is sent to the process
                (terminated with a line feed).
            max_wait_time (float): The maximum wait time in seconds to wait for
                the process to stop.
                Note that, when the process does not stop within that timeout,
                the process is stopped (which will take additional time).
            encoding (str): The encding to be used ("utf-8" is default).

        Returns:
            (tuple[list[str], list[str]]): A 2-tuple that contains `stdout` and
                `stderr` as a list of strings.
        """

        assert cmd and isinstance(cmd, list)
        assert stdin is None or isinstance(stdin, list)
        assert isinstance(max_wait_time, (int, float)) and 0 <= max_wait_time
        assert isinstance(env, dict)

        _newline = '\n'
        _space = ' '
        _sigterm_wait_time = 0.5

        log.debug("Starting process '%s' ...", _space.join(cmd))

        # Regular output.
        stdout1: str = ""
        stderr1: str = ""
        # Possible output after SIGINT.
        stdout2: str = ""
        stderr2: str = ""
        # Possible output after SIGKILL.
        stdout3: str = ""
        stderr3: str = ""

        _env = os.environ.copy()
        _env.update(env)

        try:
            process = subprocess.Popen(  # pylint: disable=R1732
                args=cmd,
                cwd=cwd,
                encoding=encoding,
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
                env=_env,
                **kwargs,
            )

            if stdin:
                _input = _newline.join(stdin) + _newline
            else:
                _input = None

            try:

                stdout1, stderr1 = process.communicate(
                    input=_input,
                    timeout=max_wait_time if 0 < max_wait_time else None)

            except subprocess.TimeoutExpired:

                try:
                    log.warning(
                        ("Process '%s' did not stop within timeout. "
                         "Sending SIGTERM ..."),
                        cmd[0])
                    process.send_signal(signal.SIGTERM)
                except Exception:  # pylint: disable=W0718
                    # Ingore exception.
                    pass

                try:
                    process.wait(_sigterm_wait_time)
                except subprocess.TimeoutExpired:
                    log.warning(
                        ("Process '%s' did not stop within timeout. "
                         "Sending SIGINT ..."),
                        cmd[0])
                    process.send_signal(signal.SIGINT)
                    stdout2, stderr2 = process.communicate()

                try:
                    process.wait(_sigterm_wait_time)
                except subprocess.TimeoutExpired:
                    log.warning(
                        ("Process '%s' did not stop within timeout. "
                         "Sending SIGKILL ..."),
                        cmd[0])
                    process.kill()
                    stdout3, stderr3 = process.communicate()

            if process.poll() is not None:
                log.info("Starting process '%s' OK. [%s]", _space.join(
                    cmd), process.returncode)
            else:
                log.error("Starting process '%s' FAILED. [%s]", _space.join(
                    cmd), process.returncode, exc_info=True)

            result = ([], [])
            if stdout1:
                result[0].extend(stdout1.splitlines())
            if stderr1:
                result[1].extend(stderr1.splitlines())
            if stdout2:
                result[0].extend(stdout2.splitlines())
            if stderr2:
                result[1].extend(stderr2.splitlines())
            if stdout3:
                result[0].extend(stdout3.splitlines())
            if stderr3:
                result[1].extend(stderr3.splitlines())
            return result

        except Exception as ex:  # pylint: disable=W0718

            log.error("Starting process '%s' FAILED. [%s]", _space.join(
                cmd), ex, exc_info=True)

            return ([], [])

    @classmethod
    def start(
        cls,
        cmd: list[str],
        wait_on_completion: bool = False,
        capture_stdout: bool = False,
        capture_stderr: bool = False,
        cwd: str | None = None,
        encoding: str | None = None,
        **kwargs,
    ) -> Process:
        """Starts a specified process and optionally waits until its completion.

        Args:
            cmd (list[str]): The process with its arguments to be started.
            capture_stdin (bool): True, if `stdin` should be captured; false,
                otherwise (default).
            capture_stdout (bool): True, if `stdout` should be captured; false,
                otherwise (default).
            capture_stderr (bool): True, if `stderr` should be captured; false,
                otherwise (default).
            cwd (str | None): The working directory of the process to be
                started. If no working directory is given, the current working
                directory of the calling process is used.
            encoding (str | None): The charset to be used for the process to
                be started. If no encoding is given,
                the current encoding of the calling process is used.

        Returns:
            Process: An instance of `Process` containing information about the
            process started.
        """

        assert cmd is not None and 0 < len(cmd)
        args = [str(arg) for arg in cmd]

        _space = ' '

        cwd = cwd or os.getcwd()
        assert os.path.exists(cwd)

        encoding = encoding or locale.getpreferredencoding(False)

        log.debug("Trying to start process... [%s]", _space.join(args))
        # pylint: disable=consider-using-with
        result = subprocess.Popen(
            args=args,
            cwd=cwd,
            encoding=encoding,
            text=True,
            bufsize=1,
            start_new_session=True,
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
                "Starting reading from pipe '%s' [%s] ...",
                process._STDOUT,
                result.pid)
            process._stdout_thread.start()

        if capture_stderr:
            process._stderr_thread = threading.Thread(
                target=process._read_stream, args=(
                    process._popen.stderr, process._STDERR)
            )
            log.debug(
                "Starting reading from pipe '%s' [%s] ...",
                process._STDERR,
                result.pid)
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
