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

"""Module media_player_client."""

import re
from threading import Lock
from typing import Callable

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from biz.dfch.scnfmixr.public.mixer import IAcquirable

from .media_player_command import MediaPlayerCommand
from .media_player_option import MediaPlayerOption
from .media_player_type import MediaPlayerType


class MediaPlayerClient(IAcquirable):
    """Wraps the `mpc` for `mpd`.

    Works with:
    * Music Player Daemon **0.23.12** (0.23.12)
    * mpc version: **0.34**
    """

    _MPC_FULLNAME = "/usr/bin/mpc"
    _MPD_HOST_ENV_NAME = "MPD_HOST"

    _type: MediaPlayerType
    _sync_root: Lock
    _is_acquired: bool
    _resource_files: list[str]

    _env: dict[str, str]

    def __init__(self, _type: MediaPlayerType):

        assert isinstance(_type, MediaPlayerType)

        self._type = _type
        self._sync_root = Lock()
        self._is_acquired = False
        self._resource_files = []

        self._env = {
            self._MPD_HOST_ENV_NAME: MediaPlayerType.get_value(_type),
        }

    def _invoke(self, cmd: list[str]) -> tuple[list[str], list[str]]:
        """Invokes the specified command and displays its output."""

        assert isinstance(cmd, list)
        assert all(isinstance(e, str) for e in cmd)

        stdout, stderr = Process.communicate(cmd, env=self._env)

        if isinstance(stdout, list) and 0 < len(stdout):
            log.debug("[%s] stdout: [%s]", self._type.name, stdout)

        if isinstance(stderr, list) and 0 < len(stderr):
            log.warning("[%s] stderr: [%s]", self._type.name, stderr)

        return (stdout, stderr)

    def _get_resource_files(self) -> list[str]:
        """Loads all resources files."""

        if 0 < len(self._resource_files):
            return self._resource_files

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.LIST_AUDIO,
        ]
        result, _ = self._invoke(cmd)

        self._resource_files = result

        return self._resource_files

    def load_resource_queue(
            self,
            predicate: Callable[[str], bool] | None = None
    ) -> list[str]:
        """Loads the current based on the result of the predicate."""

        assert predicate is None or predicate and callable(predicate)

        result: list[str] = []

        for file in self._get_resource_files():
            if not predicate(file):
                continue

            cmd = [
                self._MPC_FULLNAME,
                MediaPlayerCommand.ADD,
                file,
            ]
            result, _ = self._invoke(cmd)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.PLAYLIST,
        ]
        result, _ = self._invoke(cmd)

        return result

    def load_queue(
            self,
            predicate: Callable[[str], bool] | None = None
    ) -> list[str]:
        """Loads the current based on the result of the predicate."""

        assert predicate is None or predicate and callable(predicate)

        result: list[str] = []

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.LIST_AUDIO,
        ]
        files, _ = self._invoke(cmd)

        for file in files:
            if not predicate(file):
                continue

            cmd = [
                self._MPC_FULLNAME,
                MediaPlayerCommand.ADD,
                file,
            ]
            result, _ = self._invoke(cmd)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.PLAYLIST,
        ]
        result, _ = self._invoke(cmd)

        return result

    def get_file_info(self) -> tuple[str, int, int] | None:
        """Returns information about the currently playing file or None."""

        # [playing] #1/2   0:09/1:15 (12%)
        time_pattern = r'(?:\d+:)?\d{1,2}:\d{2}'

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.STATUS,
        ]
        stdout, _ = self._invoke(cmd)

        if not isinstance(stdout, list) or 3 != len(stdout):
            log.debug("Incorrect stdout [type %s] [len %s].", type(
                stdout), len(stdout))
            return None

        filename = stdout[0]

        text = stdout[1]
        matches = re.findall(time_pattern, text)
        if 2 != len(matches):
            log.debug("Incorrect matches [matches '%s'].", matches)
            return None

        current_time, total_time = matches
        log.debug("Matches [current_time '%s'] [total_time '%s']",
                  current_time, total_time)

        current_seconds = self.time_to_seconds(current_time)
        if current_seconds is None:
            log.debug("Time [current_seconds '%s']", current_seconds)
            return None

        total_seconds = self.time_to_seconds(total_time)
        if total_seconds is None:
            log.debug("Time [total_seconds '%s']", total_seconds)
            return None

        result = (filename, current_seconds, total_seconds)

        return result

    def time_to_seconds(self, value: str) -> int | None:
        """Returns seconds from time."""

        parts = value.split(':')

        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)

        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

        return None

    def set_repeat(self, value: bool) -> None:
        """Sets or unsets the 'repeat' setting of the queue."""

        assert isinstance(value, bool)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.REPEAT,
            MediaPlayerOption.ON if value else MediaPlayerOption.OFF,
        ]
        self._invoke(cmd)

    def set_random(self, value: bool) -> None:
        """Sets or unsets the 'random' setting of the queue."""

        assert isinstance(value, bool)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.RANDOM,
            MediaPlayerOption.ON if value else MediaPlayerOption.OFF,
        ]
        self._invoke(cmd)

    def set_consume(self, value: bool) -> None:
        """Sets or unsets the 'consume' setting of the queue."""

        assert isinstance(value, bool)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.CONSUME,
            MediaPlayerOption.ON if value else MediaPlayerOption.OFF,
        ]
        self._invoke(cmd)

    def set_single(self, value: bool) -> None:
        """Sets or unsets the 'single' setting of the queue."""

        assert isinstance(value, bool)

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.SINGLE,
            MediaPlayerOption.ON if value else MediaPlayerOption.OFF,
        ]
        self._invoke(cmd)

    def start(self):
        """Transport control: start."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.START,
        ]
        self._invoke(cmd)

    def stop(self):
        """Transport control: stop."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.STOP,
        ]
        self._invoke(cmd)

    def pause(self):
        """Transport control: pause."""

        with self._sync_root:
            self._is_paused = not self._is_paused

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.PAUSE,
        ]
        self._invoke(cmd)

    def clear(self):
        """Transport control: stop. Playlist control: clear."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.CLEAR,
        ]
        self._invoke(cmd)

    def seek_start(self):
        """Transport control: start of clip."""

        self.seek_absolute(0)

    def seek_end(self, value: int = 10):
        """Transport control: end of clip."""

        assert isinstance(value, int) and 0 <= value

        result = self.get_file_info()
        if result is None:
            return

        _, _, total = result

        end_point = max(total - value, 0)
        self.seek_absolute(end_point)

    def seek_absolute(self, value: int):
        """Transport control: start."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.SEEK,
            str(value),
        ]
        self._invoke(cmd)

    def seek_relative(self, value: int):
        """Transport control: start."""

        if 0 == value:
            return

        if 0 <= value:
            position = f"+{value}"
        else:
            position = f"{value}"

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.SEEK,
            position,
        ]
        self._invoke(cmd)

    def next(self):
        """Playlist control: next."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.NEXT,
        ]
        self._invoke(cmd)

    def previous(self):
        """Playlist control: previous."""

        cmd = [
            self._MPC_FULLNAME,
            MediaPlayerCommand.PREVIOUS,
        ]
        self._invoke(cmd)

    @property
    def is_acquired(self):
        return self._is_acquired

    @is_acquired.setter
    def is_acquired(self, value):

        assert isinstance(value, bool)

        self.is_acquired = value

    def acquire(self):

        if self._is_acquired:
            return self

        with self._sync_root:

            if self._is_acquired:
                return self

            log.debug("Mpc: Acquiring resource '%s' ...", self._type.name)

            cmd = [
                self._MPC_FULLNAME,
                MediaPlayerCommand.UPDATE,
            ]
            self._invoke(cmd)

            cmd = [
                self._MPC_FULLNAME,
                MediaPlayerCommand.CLEAR,
            ]
            self._invoke(cmd)

            self._is_acquired = True

            log.info("Mpc: Acquiring resource '%s' OK.", self._type.name)

            return self

    def release(self):
        if not self._is_acquired:
            return

        with self._sync_root:

            if not self._is_acquired:
                return

            log.debug("Mpc: Releasing resource ...")

            # Clearing the queue automatically stops playing.
            cmd = [
                self._MPC_FULLNAME,
                MediaPlayerCommand.CLEAR,
            ]
            self._invoke(cmd)

            self._is_acquired = False

            log.info("Mpc: Releasing resource OK.")
