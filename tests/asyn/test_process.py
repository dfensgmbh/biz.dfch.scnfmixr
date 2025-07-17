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

"""Contains platform specific tests."""

import unittest
import os

from biz.dfch.asyn import Process


class TestProcess(unittest.TestCase):
    """Testing Process class."""

    _NT: str = "nt"
    _POSIX: str = "posix"

    def test_start_with_invalid_program_throws(self):
        """Starting an non-existing command fails."""

        args = [
            "invalid-process-name",
        ]

        with self.assertRaises(FileNotFoundError):
            _ = Process.start(args, True)

    def test_start_sync_windows_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, wait_on_completion=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

    def test_start_sync_linux_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._POSIX != os.name:
            self.skipTest(f"This test needs to run on {self._POSIX}.")

        args = ["/usr/bin/ls"]

        sut = Process.start(args, wait_on_completion=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

    def test_start_async_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            "Start-Sleep 3",
        ]

        sut = Process.start(args, wait_on_completion=False)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_running)

        result = sut.stop()
        self.assertFalse(sut.is_running)
        self.assertTrue(result)

    def test_start_async_linux_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._POSIX != os.name:
            self.skipTest(f"This test needs to run on {self._POSIX}.")

        args = [
            "/usr/bin/sleep",
            "3",
        ]

        sut = Process.start(args, wait_on_completion=False)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_running)

        result = sut.stop()
        self.assertFalse(sut.is_running)
        self.assertTrue(result)

    def test_start_sync_with_exit_code_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        expected = 42
        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            f"exit {expected}",
        ]

        sut = Process.start(args, wait_on_completion=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.exit_code
        self.assertEqual(expected, result)

    def test_start_sync_with_reading_from_stdout_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=True,
                            capture_stderr=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

    def test_reading_from_stdout_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=True,
                            capture_stderr=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.stdout
        self.assertTrue(0 < len(result))

        result = sut.stdout
        self.assertEqual(0, len(result))

    def test_reading_from_stderr_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            "Write-Error 'arbitrary-message'",
        ]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=True,
                            capture_stderr=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.stderr
        self.assertTrue(0 < len(result))

        result = sut.stderr
        self.assertEqual(0, len(result))

    def test_reading_from_stderr_without_capture_returns_empty(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            "Write-Error 'arbitrary-error'; Write-Output 'arbitrary-message'",
        ]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=True,
                            capture_stderr=False)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.stderr
        self.assertEqual(0, len(result))

        result = sut.stderr
        self.assertEqual(0, len(result))

    def test_reading_from_output_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=True,
                            capture_stderr=True)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.output
        self.assertTrue(0 < len(result))

        result = sut.output
        self.assertEqual(0, len(result))
        self.assertEqual(0, len(sut.stdout))
        self.assertEqual(0, len(sut.stderr))

    def test_reading_from_output_without_capture_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = ["C:\\Windows\\system32\\cmd.exe", "/c", "dir"]

        sut = Process.start(args, wait_on_completion=True, capture_stdout=False,
                            capture_stderr=False)

        self.assertIsNotNone(sut)
        self.assertFalse(sut.is_running)

        result = sut.output
        self.assertEqual(0, len(result))

        self.assertEqual(0, len(sut.stdout))
        self.assertEqual(0, len(sut.stderr))

    def test_stop_windows_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._NT != os.name:
            self.skipTest(f"This test needs to run on {self._NT}.")

        args = [
            "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "-Command",
            "Start-Sleep 15",
        ]

        sut = Process.start(args, wait_on_completion=False)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_running)

        result = sut.stop(max_wait_time=1, force=True)

        self.assertTrue(result)
        self.assertFalse(sut.is_running)

        # Process already stopped.
        result = sut.stop(max_wait_time=1, force=True)
        self.assertFalse(result)

    def test_stop_linux_succeeds(self):
        """This test is **OS/platform specific**"""

        if self._POSIX != os.name:
            self.skipTest(f"This test needs to run on {self._POSIX}.")

        args = [
            "/usr/bin/sleep",
            "15",
        ]

        sut = Process.start(args, wait_on_completion=False)

        self.assertIsNotNone(sut)
        self.assertTrue(sut.is_running)

        result = sut.stop(max_wait_time=1, force=True)

        self.assertTrue(result)
        self.assertFalse(sut.is_running)

        # Process already stopped.
        result = sut.stop(max_wait_time=1, force=True)
        self.assertFalse(result)

    def test_stdin_with_input_succeeds(self):
        """Testing stdin with input succeeds."""

        if self._POSIX != os.name:
            self.skipTest(f"This test needs to run on {self._POSIX}.")

        cmd = [
            "/usr/bin/jack_transport",
        ]
        stdin = [
            "play",
            "exit",
        ]

        stdout, _ = Process.communicate(cmd, stdin)

        self.assertTrue("jack_transport>" in stdout[0])
        self.assertEqual(2, len(stdout), stdout)

    def test_stdin_without_input_succeeds(self):
        """Testing stdin without input succeeds."""

        if self._POSIX != os.name:
            self.skipTest(f"This test needs to run on {self._POSIX}.")

        cmd = [
            "/usr/bin/jack_lsp",
        ]

        stdout, stderr = Process.communicate(cmd)

        self.assertTrue("system:capture_1" in stdout[0])
