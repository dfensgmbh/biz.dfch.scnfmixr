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

import asyncio
import os
from typing import Optional

from src.Asyn import Process1

__all__ = ["Process2"]


class Process2:
    """Class that supports starting external processes. Use static `start` method to start processes."""

    _STDOUT = "stdout"
    _STDERR = "stderr"

    @staticmethod
    async def start(cmd: list[str], cwd: Optional[str] = None, wait_on_completion: bool = False, **kwargs) -> Process1:
        """Start an external process and returns a `Process` object.
        Args:
            cmd (list[str]): The process to start.
                The program name and its arguments must be passed as a list of strings.
            cwd (str, optional): The working directory for the process.
                If not specified, `os.getcwd()` is used. The path will be asserted if it exists.
            wait_on_completion (bool, optional): If True, waits for the process to complete before returning.
                Defaults to `False`.
            **kwargs: Additional keyword arguments passed to the underlying process creation logic.
        Returns:
            Process: An object containing information about the started process.
        """

        if cwd is None:
            cwd = os.getcwd()
        assert os.path.exists(cwd)

        coroutine = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
            cwd=cwd,
            **kwargs,
        )

        process_info = Process1(coroutine)

        if wait_on_completion:
            coroutine.wait()

        return process_info
