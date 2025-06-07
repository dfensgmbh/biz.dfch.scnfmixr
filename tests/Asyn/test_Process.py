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

import unittest

from Asyn import Process


class TestProcess(unittest.TestCase):

    def test_start_with_invalid_program_throws(self):

        args = [
            "invalid-process-name",
        ]

        with self.assertRaises(FileNotFoundError):
            _ = Process.start(args, True)

    def test_start_sync_succeeds(self):
        """This test is **OS/platform specific**"""

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

    def test_start_async_succeeds(self):
        """This test is **OS/platform specific**"""

        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            "Start-Sleep 1",
        ]

        sut = Process.start(args, False)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_running)

    def test_start_sync_with_exit_code_succeeds(self):
        """This test is **OS/platform specific**"""

        expected = 42
        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            f"exit {expected}",
        ]

        sut = Process.start(args, True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.exit_code
        self.assertEqual(expected, result)

    def test_start_sync_with_reading_from_stdout_succeeds(self):
        """This test is **OS/platform specific**"""

        args = [
            "C:\\Windows\\system32\\ping.exe",
            "-n",
            "5",
            "www.google.com",
        ]

        sut = Process.start(args, wait_on_completion=True, redirect_stdout=True, redirect_stderr=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)
