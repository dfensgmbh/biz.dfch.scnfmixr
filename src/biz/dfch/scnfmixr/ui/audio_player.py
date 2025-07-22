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

"""Module defining the audio player for output handling."""

from dataclasses import dataclass
from enum import StrEnum
import threading
import time

from biz.dfch.logging import log
from biz.dfch.asyn import (
    Process,
    ConcurrentDoubleSideQueueT,
)

from ..public.messages import AudioMixer as msgt
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..system import MessageQueue


__all__ = [
    "AudioPlayer",
]


@dataclass(frozen=True)
class AudioItem:
    """Audio info."""
    type: type
    path: str
    name: StrEnum
    is_loop: bool


class AudioPlayer:
    """Defines the audio player for output handling."""

    _WAIT_INTERVAL_MS: int = 250
    _KEEP_ALIVE_INTERVAL_MS: int = 10 * 1000

    _ECASOuND_FULLNAME = "/usr/bin/ecasound"
    _ECASOuND_OUTPUT_NAME = "jack"
    _ECASOuND_PORT_NAME = "AudioPlayer"
    _ECASOUND_OPTION_SEP = ":"
    _ECASOUND_OPTION_DELIMITER = ","
    _ECASOUND_OPTION_QUIET = "-q"
    _ECASOUND_OPTION_GLOBAL = "-G"
    _ECASOUND_OPTION_INPUT = "-i"
    _ECASOUND_OPTION_AUDIOLOOP = "audioloop"
    _ECASOUND_OPTION_OUTPUT = "-o"
    _ECASOUND_OPTION_TRANSPORT_NO = "notransport"

    _message_queue: MessageQueue
    _process: Process
    _do_cancel_worker: bool
    _do_cancel_item: bool
    _queue: ConcurrentDoubleSideQueueT[AudioItem]
    _signal_queue: threading.Event
    _jack_name: str
    _thread: threading.Thread

    def __init__(self, jack_name: str) -> None:
        """Returns an instance of this class."""

        assert jack_name and jack_name.strip()

        self._process = None
        self._do_cancel_worker = False
        self._do_cancel_item = False
        self._queue = ConcurrentDoubleSideQueueT[AudioItem]()
        self._signal_queue = threading.Event()
        self._signal_queue.clear()
        self._jack_name = jack_name

        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

        self._message_queue = MessageQueue.Factory.get()
        self._message_queue.register(
            self.on_message,
            lambda e: isinstance(
                e,
                (msgt.DefaultOutputChangedNotification,
                 SystemMessage.UiEventInfoAudioMessage,
                 SystemMessage.Shutdown)))

    def on_message(self, message: MessageBase) -> None:
        """Message handler."""

        log.debug("'%s' [%s]", message.name, type(message))

        assert isinstance(message,
                          (msgt.DefaultOutputChangedNotification,
                           SystemMessage.UiEventInfoAudioMessage,
                           SystemMessage.Shutdown))

        if isinstance(message, SystemMessage.UiEventInfoAudioMessage):

            item = AudioItem(
                type=message.type,
                path=message.path,
                name=message.value.name,
                is_loop=message.value.is_loop,
            )

            if message.type is SystemMessage.UiEventInfoStateEnterMessage:
                self._queue.clear()

            log.debug(
                "Trying to enqueue item '%s' [loop=%s]",
                item.path,
                item.is_loop)

            self._queue.enqueue(item)
            self._signal_queue.set()

            return

        if isinstance(message, msgt.DefaultOutputChangedNotification):
            if message.value != self._jack_name:
                log.debug("Changing output value form '%s' to '%s'.",
                          message.value, self._jack_name)
                self._jack_name = message.value
            return

        if isinstance(message, SystemMessage.Shutdown):
            # For later: switch sound to ALSA output?
            # Maybe even better: have AlsaMixer signal
            # DefaultOutputChangedNotification?
            self._do_cancel_worker = True
            return

    def _worker(self):
        """The worker thread that plays and stops the audio files.

        Args:
            None:

        Returns:
            None:
        """

        log.debug("Initialising worker ...")

        current_item: AudioItem = None

        log.info("Initialising worker OK.")

        start_time = time.monotonic()
        while not self._do_cancel_worker:

            try:

                # Check if there is something to process ...
                item = self._queue.peek()

                # ... only then wait for the signal.
                if item is None:

                    # Waiting for signal ...
                    result = self._signal_queue.wait(
                        self._WAIT_INTERVAL_MS/1000)
                    self._signal_queue.clear()
                    # ... and exit if timeout.
                    if not result:
                        now = time.monotonic()
                        if now > (
                                start_time + self._KEEP_ALIVE_INTERVAL_MS/1000):
                            log.debug("Worker keep alive. [%s]",
                                      len(self._queue))
                            start_time = now
                        continue

                    # We have to check here again, as the signal could have been
                    # set, to indicate exit.
                    if self._do_cancel_worker:
                        break

                    # ... otherwise check if there is soemthing to process.
                    item = self._queue.peek()

                    # This really should not happen.
                    if item is None:

                        log.warning("Empty queue after signal set. [%s]",
                                    len(self._queue))
                        continue

                # If there is a running proces ...
                if self._process is not None and self._process.is_running:

                    # ... and that process is a loop ...
                    assert current_item
                    if current_item.is_loop:

                        # .. stop the process.
                        pid = self._process.pid

                        log.debug(
                            "Cancelling currently playing item [%s] ...",
                            pid)

                        result = self._process.stop(force=True)
                        self._process = None

                        log.info(
                            "Cancelling currently playing item [%s] OK. [%s]",
                            pid,
                            result)

                    # ... if not, wait for the process to stop playing.
                    else:

                        self._process._popen.wait()
                        self._process = None

                # No process at this point, so we can start playing next
                # audio ...
                assert self._process is None, self._process.pid

                # Get the item to process ...
                item = self._queue.dequeue()
                if item is None:
                    log.warning("Empty queue after peek. [%s]",
                                len(self._queue))
                    continue

                # ... and set it as our current item.
                current_item = item

                # If current item is loop and there is another item in the
                # queue, skip it and continue with next iteration.
                if current_item.is_loop:
                    if not self._queue.is_empty():
                        continue

                # Now play the audio item.
                self._process = self._play(current_item)

            except Exception as ex:  # pylint: disable=W0718

                log.error("Exception occurred in worker. [%s]",
                          ex, exc_info=True)

                try:
                    # Clean up any "left over" process info.
                    if (self._process and
                            self._process._popen.poll is not None):
                        self._process = None
                except:  # pylint: disable=W0702  # noqa: E722
                    pass

                continue

        log.info("Worker stopped.")

    def _play(self, item: AudioItem) -> Process:
        """Plays an audio item."""

        assert isinstance(item, AudioItem)

        file = item.path

        log.info(
            "Trying to play '%s' [loop=%s] to '%s' ...",
            file,
            item.is_loop,
            self._jack_name)

        cmd: list[str] = []
        cmd.append(self._ECASOuND_FULLNAME)
        cmd.append(self._ECASOUND_OPTION_QUIET)
        cmd.append(
            f"{self._ECASOUND_OPTION_GLOBAL}"
            f"{self._ECASOUND_OPTION_SEP}"
            f"{self._ECASOuND_OUTPUT_NAME}"
            f"{self._ECASOUND_OPTION_DELIMITER}"
            f"{self._ECASOuND_PORT_NAME}"
            f"{self._ECASOUND_OPTION_DELIMITER}"
            f"{self._ECASOUND_OPTION_TRANSPORT_NO}"
        )
        cmd.append(self._ECASOUND_OPTION_INPUT)
        if item.is_loop:
            cmd.append(
                f"{self._ECASOUND_OPTION_AUDIOLOOP}"
                f"{self._ECASOUND_OPTION_DELIMITER}"
                f"{file}"
            )
        else:
            cmd.append(file)
        cmd.append(self._ECASOUND_OPTION_OUTPUT)
        cmd.append(
            f"{self._ECASOuND_OUTPUT_NAME}"
            f"{self._ECASOUND_OPTION_DELIMITER}"
            f"{self._jack_name}")

        return Process.start(cmd)

    def stop(self) -> None:
        """Clears the audio queue, stops the playing item (if any) and stops
        the worker thread. This is a blocking call that only returns when
        processing has completely stopped.

        Attributes:
            None:

        Returns:
            None:
        """

        log.info("Stopping queue ...")

        self.clear(True)

        self._do_cancel_worker = True
        self._thread.join()

    def clear(self, do_stop_active_item: bool = False) -> None:
        """Clears the internal audio queue.

        Attributes:
            do_stop_active_item (bool): True, if the currently playing item
                shall be stopped (if there is one); false otherwise.
        Returns:
            None:
        """

        log.debug("Clearing queue ...")

        _ = do_stop_active_item
        self._queue.clear()

        log.info("Clearing queue OK.")

    def enqueue(self, item: AudioItem) -> None:
        """Enqueues an item in the audio queue.

        Attributes:
            item (AudioItem): An item to enqueue into the audio player.

        Returns:
            None:
        """

        assert isinstance(item, AudioItem)

        log.debug(
            "Trying to enqueue item '%s' [loop=%s]", item.path, item.is_loop)

        self._queue.enqueue(item)
