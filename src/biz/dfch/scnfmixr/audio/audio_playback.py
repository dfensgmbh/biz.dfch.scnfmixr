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

"""Module audio_playback."""

from __future__ import annotations
from threading import Event, Lock, Thread
import time
from typing import ClassVar

from biz.dfch.logging import log
from biz.dfch.asyn import ConcurrentDoubleSideQueueT

from ..system import MessageQueue
from ..public.mixer import IAcquirable
from ..public.messages import MessageBase, SystemMessage
from ..public.messages.audio_playback import IAudioPlaybackMessage
from ..public.messages.audio_playback import AudioPlayback as msgt

__all__ = [
    "AudioPlayback",
]


class AudioPlayback(IAcquirable):
    """The audio playback player."""

    _WORKER_SIGNAL_WAIT_TIME_MS = 5000
    _EXCEPTION_TIMEOUT_MS = 1000

    _is_acquired: bool
    _sync_root: Lock
    _signal: Event
    _worker_do_stop: bool
    _mq: MessageQueue
    _worker_thread: Thread
    _queue: ConcurrentDoubleSideQueueT[IAudioPlaybackMessage]

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not AudioPlayback.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._is_acquired = True
        self._sync_root = Lock()
        self._signal = Event()
        self._mq = MessageQueue()
        self._worker_do_stop = False
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._queue = ConcurrentDoubleSideQueueT[IAudioPlaybackMessage]()

        log.info("Initialising OK.")

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AudioPlayback] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> AudioPlayback:
            """Creates or gets the instance of the audio playback player."""

            if AudioPlayback.Factory.__instance is not None:
                return AudioPlayback.Factory.__instance

            with AudioPlayback.Factory._sync_root:

                if AudioPlayback.Factory.__instance is not None:
                    return AudioPlayback.Factory.__instance

                AudioPlayback.Factory.__instance = AudioPlayback()

            AudioPlayback.Factory.__instance.acquire()
            return AudioPlayback.Factory.__instance

    def _worker(self) -> None:
        """Worker thread for processing messages."""

        log.debug("_worker: Initialising ...")

        signal_wait_time_s = self._WORKER_SIGNAL_WAIT_TIME_MS / 1000

        start = time.monotonic()

        log.info("_worker: Initialising OK.")

        log.debug("_worker: Executing ...")

        while not self._worker_do_stop:
            try:
                now = time.monotonic()
                if now > start + signal_wait_time_s:
                    delta = now - start
                    start = now
                    log.debug("_worker: Waiting [%sms].", int(delta*1000))

                result = self._signal.wait(signal_wait_time_s)
                self._signal.clear()
                if not result:
                    continue

                msg = self._queue.dequeue()
                if msg is None:
                    continue

                log.debug(
                    "_worker: Processing message '%s' [%s] ...",
                    type(msg),
                    msg.name)

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

        if isinstance(message, msgt.PlaybackStartCommand):
            return

        if isinstance(message, msgt.PlaybackStopCommand):
            return

        if isinstance(message, msgt.PauseResumeCommand):
            return

        if isinstance(message, msgt.ClipStartCommand):
            return

        if isinstance(message, msgt.ClipPreviousCommand):
            return

        if isinstance(message, msgt.ClipNextCommand):
            return

        if isinstance(message, msgt.CuePointPreviousCommand):
            return

        if isinstance(message, msgt.ClipNextCommand):
            return

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
