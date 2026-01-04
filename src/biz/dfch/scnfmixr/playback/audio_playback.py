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

"""Module audio_playback."""

from __future__ import annotations
import bisect
from threading import Event, Lock, Thread
import time
from typing import ClassVar, Callable, Any

from biz.dfch.logging import log
from biz.dfch.asyn import ConcurrentDoubleSideQueueT, Process

from text import MultiLineTextParser

from ..system import MessageQueue
from ..public.mixer import IAcquirable
from ..public.storage import MountPoint
from ..public.messages import MessageBase, SystemMessage
from ..public.messages.audio_playback import IAudioPlaybackMessage
from ..public.messages.audio_playback import AudioPlayback as msgt

from .metaflac_visitor import MetaflacVisitor
from .media_player_type import MediaPlayerType
from .media_player_client import MediaPlayerClient

__all__ = [
    "AudioPlayback",
]


class AudioPlayback(IAcquirable):
    """The audio playback player."""

    _WORKER_SIGNAL_WAIT_TIME_MS = 10000
    _EXCEPTION_TIMEOUT_MS = 1000

    _message_handler: dict[type, Callable[[Any], None]]

    _is_acquired: bool
    _sync_root: Lock
    _signal: Event
    _worker_do_stop: bool
    _mq: MessageQueue
    _worker_thread: Thread
    _queue: ConcurrentDoubleSideQueueT[IAudioPlaybackMessage]
    _is_playing: bool
    _client: MediaPlayerClient | None
    _queued_items: dict[str, list[int]]

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not AudioPlayback.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initializing ...")

        self._is_acquired = False
        self._sync_root = Lock()
        self._signal = Event()
        self._mq = MessageQueue.Factory.get()
        self._worker_do_stop = False
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._queue = ConcurrentDoubleSideQueueT[IAudioPlaybackMessage]()
        self._is_playing = False
        self._client = None
        self._queued_items: dict[str, list[int]] = {}

        self._message_handler: dict[type, Callable[[Any], None]] = {
            msgt.PlaybackStartCommand: self._on_playback_start,
            msgt.PlaybackStopCommand: self._on_playback_stop,
            msgt.PauseResumeCommand: self._on_playback_pause,
            msgt.ClipStartCommand: self._on_playback_clip_start,
            msgt.ClipEndCommand: self._on_playback_clip_end,
            msgt.ClipPreviousCommand: self._on_playback_clip_previous,
            msgt.ClipNextCommand: self._on_playback_clip_next,
            msgt.CuePointPreviousCommand: self._on_playback_cue_point_previous,
            msgt.CuePointNextCommand: self._on_playback_cue_point_next,
            msgt.SeekNextCommand: self._on_playback_seek_next,
            msgt.SeekPreviousCommand: self._on_playback_seek_previous,
        }

        log.info("Initializing OK.")

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AudioPlayback] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> AudioPlayback:
            """Creates or gets the instance of the audio playback player.

            After the call returns, the instance is acquired.
            """

            if AudioPlayback.Factory.__instance is not None:
                return AudioPlayback.Factory.__instance

            with AudioPlayback.Factory._sync_root:

                if AudioPlayback.Factory.__instance is not None:
                    return AudioPlayback.Factory.__instance

                AudioPlayback.Factory.__instance = AudioPlayback()

            # Note: here we acquire the class directly after creating the
            # singleton, which might not be totally intuitive! On the other hand
            # it does not make sense to get the singleton and acquire each time
            # after it.
            AudioPlayback.Factory.__instance.acquire()

            return AudioPlayback.Factory.__instance

    def _worker(self) -> None:
        """Worker thread for processing messages."""

        log.debug("_worker: Initializing ...")

        signal_wait_time_s = self._WORKER_SIGNAL_WAIT_TIME_MS / 1000

        start = time.monotonic()

        log.info("_worker: Initializing OK.")

        log.debug("_worker: Executing ...")

        while not self._worker_do_stop:
            try:
                now = time.monotonic()
                if now > start + signal_wait_time_s:
                    delta = now - start
                    start = now
                    log.debug("_worker: Keep alive [%sms].", int(delta*1000))

                result = self._signal.wait(signal_wait_time_s)
                self._signal.clear()
                if not result:
                    continue

                while True:
                    message = self._queue.dequeue()
                    if message is None:
                        break

                    handler = self._message_handler.get(type(message))
                    if handler is None:
                        log.warning("_worker: Unrecognized message: '%s' [%s].",
                                    type(message).__name__,
                                    message.name)
                        continue

                    log.debug(
                        "_worker: Processing message '%s' [%s] ...",
                        type(message).__name__,
                        message.name)

                    handler(message)

                    log.info(
                        "_worker: Processing message '%s' [%s] OK.",
                        type(message).__name__,
                        message.name)

            except Exception as ex:  # pylint: disable=W0718
                log.error("_worker: An error occurred: '%s'. Waiting %sms ...",
                          ex,
                          self._EXCEPTION_TIMEOUT_MS,
                          exc_info=True)
                time.sleep(self._EXCEPTION_TIMEOUT_MS / 1000)

        log.info("_worker: Executing OK.")

    def _on_message(self, message: MessageBase):
        """Message handler."""

        if isinstance(message, SystemMessage.Shutdown):
            self.release()
            return

        log.debug("Message type: '%s'", type(message))

        if isinstance(message, IAudioPlaybackMessage):
            self._queue.enqueue(message)
            self._signal.set()
            return

        log.warning("Unrecognized message received: '%s' [%s].",
                    type(message).__name__,
                    message.name)

    def _on_playback_start(self, message: msgt.PlaybackStartCommand) -> None:
        """PlaybackStartCommand"""

        assert isinstance(message, msgt.PlaybackStartCommand)

        self._client = MediaPlayerClient(MediaPlayerType.PLAYBACK)
        self._client.acquire()
        self._client.set_repeat(True)

        # Load audio files from only the first available storage device (RC1 or
        # RC2).
        _queued_items = self._client.load_playback_queue(
            lambda e: e.lower().startswith(MountPoint.RC1.name.lower()))
        assert isinstance(_queued_items, list)

        if 0 == len(_queued_items):
            _queued_items = self._client.load_playback_queue(
                lambda e: e.lower().startswith(MountPoint.RC2.name.lower()))
        assert isinstance(_queued_items, list)

        log.debug("Currently queued items: [%s]", _queued_items)

        for item in _queued_items:

            fullname = self.get_fullname(item)

            log.debug(fullname)

            seek_points = self.get_seekpoints(fullname)

            self._queued_items[item] = seek_points

            log.debug("Item '%s': [%s]", item, self._queued_items[item])

        self._client.start()
        self._is_playing = True

    def get_fullname(self, value: str) -> str:
        """Returns the full path based on value from `MountPoint`."""

        assert isinstance(value, str) and value.strip()

        value_lower = value.lower()
        for mp in MountPoint:
            mp_lower = mp.name.lower()
            if not value_lower.startswith(mp_lower):
                continue

            return f"{mp.value}{value.removeprefix(mp_lower)}"

    def get_seekpoints(self, fullname: str) -> list[int]:
        """Returns the seekpoints in seconds based on the sample rate from the
        specified file."""

        assert isinstance(fullname, str) and fullname.lower().endswith(".flac")

        cmd = [
            "/usr/bin/metaflac",
            "--list",
            fullname,
        ]
        text, _ = Process.communicate(cmd)

        visitor = MetaflacVisitor()
        dic = {
            MetaflacVisitor.METADATA_BLOCK: visitor.process_metadata_block,
            MetaflacVisitor.STREAM_INFO: visitor.process_stream_info,
            MetaflacVisitor.SAMPLE_RATE: visitor.process_sample_rate,
            MetaflacVisitor.SEEK_TABLE: visitor.process_seek_table,
            MetaflacVisitor.SEEK_POINT: visitor.process_seek_point,
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=2,
            dic=dic)
        parser.parse(text)

        unique = set()
        for item in visitor.items:
            unique.add(item)

        result = sorted(list(unique))

        return result

    def _on_playback_stop(self, message: msgt.PlaybackStopCommand) -> None:
        """PlaybackStopCommand"""

        assert isinstance(message, msgt.PlaybackStopCommand)

        self._client.release()
        self._is_playing = False

    def _on_playback_pause(self, message: msgt.PauseResumeCommand) -> None:
        """PauseResumeCommand"""

        assert isinstance(message, msgt.PauseResumeCommand)

        with self._sync_root:
            is_currently_playing = self._is_playing
            self._is_playing = not self._is_playing

        if is_currently_playing:
            self._client.pause()
        else:
            self._client.start()

    def _on_playback_seek_next(self, message: msgt.SeekNextCommand) -> None:
        """SeekNextCommand"""

        assert isinstance(message, msgt.SeekNextCommand)

        if not self._is_playing:
            return

        self._client.seek_relative(message.value)

    def _on_playback_seek_previous(
            self,
            message: msgt.SeekPreviousCommand) -> None:
        """SeekPreviousCommand"""

        assert isinstance(message, msgt.SeekPreviousCommand)

        if not self._is_playing:
            return

        self._client.seek_relative(message.value)

    def _on_playback_clip_start(self, message: msgt.ClipStartCommand) -> None:
        """ClipStartCommand"""

        assert isinstance(message, msgt.ClipStartCommand)

        if not self._is_playing:
            return

        self._client.seek_start()

    def _on_playback_clip_end(self, message: msgt.ClipEndCommand) -> None:
        """ClipEndCommand"""

        assert isinstance(message, msgt.ClipEndCommand)

        if not self._is_playing:
            return

        self._client.seek_end()

    def _on_playback_clip_next(self, message: msgt.ClipNextCommand) -> None:
        """ClipNextCommand"""

        assert isinstance(message, msgt.ClipNextCommand)

        if not self._is_playing:
            return

        self._client.next()

    def _on_playback_clip_previous(
            self,
            message: msgt.ClipPreviousCommand) -> None:
        """ClipPreviousCommand"""

        assert isinstance(message, msgt.ClipPreviousCommand)

        if not self._is_playing:
            return

        self._client.previous()

    def _on_playback_cue_point_next(
            self,
            message: msgt.CuePointNextCommand) -> None:
        """CuePointNextCommand"""

        assert isinstance(message, msgt.CuePointNextCommand)

        if not self._is_playing:
            return

        result = self._client.get_file_info()
        if result is None:
            log.debug("CuePointNextCommand: No file info. "
                      "Jumping end of clip.")
            self._client.seek_end()
            return

        filename, current, total = result
        log.debug(("CuePointNextCommand: [filename: %s] "
                   "[current: %s] [total: %s]."),
                  filename, current, total)

        seek_points = self._queued_items.get(filename)
        pos = bisect.bisect_right(seek_points, current)

        if pos >= len(seek_points):

            log.debug("CuePointNextCommand: No file info. "
                      "Jumping end of clip.")
            self._client.seek_end()
            return

        seek_point = seek_points[pos]

        log.debug(("Seeking this seek point '%s' [current: '%s'] "
                   "[seek_points: %s]."),
                  seek_point, current, seek_points)

        self._client.seek_absolute(seek_point)

    def _on_playback_cue_point_previous(
            self,
            message: msgt.CuePointPreviousCommand) -> None:
        """CuePointPreviousCommand"""

        assert isinstance(message, msgt.CuePointPreviousCommand)

        if not self._is_playing:
            return

        result = self._client.get_file_info()
        if result is None:
            log.debug("CuePointPreviousCommand: No file info. "
                      "Jumping start of clip.")
            self._client.seek_start()
            return

        filename, current, total = result
        log.debug(("CuePointPreviousCommand: [filename: %s] "
                   "[current: %s] [total: %s]."),
                  filename, current, total)

        seek_points = self._queued_items.get(filename)
        pos = bisect.bisect_left(seek_points, current)

        if 0 == pos:
            log.debug("CuePointPreviousCommand: No previous seek point. "
                      "Jumping start of clip.")
            self._client.seek_start()
            return

        seek_point = seek_points[pos - 1]

        log.debug(("Seeking this seek point '%s' [current: '%s'] "
                  "[seek_points: %s]."),
                  seek_point, current, seek_points)

        self._client.seek_absolute(seek_point)

    @property
    def is_acquired(self):
        return self._is_acquired

    @is_acquired.setter
    def is_acquired(self, value):

        assert isinstance(value, bool)

        self._is_acquired = value

    def acquire(self):
        if self._is_acquired:
            return self

        with self._sync_root:
            if self._is_acquired:
                return self

            log.debug("Acquiring resources ...")

            self._is_playing = False
            self._worker_do_stop = False
            self._signal.clear()
            self._worker_thread.start()
            self._mq.register(
                self._on_message,
                lambda e: isinstance(e, (SystemMessage.Shutdown,
                                         IAudioPlaybackMessage)))

            self._is_acquired = True

        log.info("Acquiring resources OK.")

        return self

    def release(self):
        if not self._is_acquired:
            return

        with self._sync_root:
            if not self._is_acquired:
                return

            log.debug("Releasing resources ...")

            self._mq.unregister(self._on_message)
            self._worker_do_stop = True
            self._worker_thread.join()

            self._is_acquired = False

        log.info("Releasing resources OK.")
