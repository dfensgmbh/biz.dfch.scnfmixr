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

import queue
import threading
import time

from biz.dfch.logging import log
from biz.dfch.asyn import Process

from ..mixer import AudioMixer

__all__ = [
    "AudioPlayer",
]


class AudioPlayer:
    """Defines the audio player for output handling."""

    WAIT_INTERVAL_MS: int = 250

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
    _ECASOUND_OPTION_LOOP = "-tl"
    _ECASOUND_OPTION_TRANSPORT_NO = "notransport"

    _process: Process
    _do_cancel_worker: threading.Event
    _do_cancel_item: bool
    _queue: queue.Queue[tuple[str, bool]]
    _jack_name: str
    _thread: threading.Thread

    def __init__(self, jack_name: str) -> None:
        """Returns an instance of this class."""

        assert jack_name and jack_name.strip()

        self._process = None
        self._do_cancel_worker = threading.Event()
        self._do_cancel_item = False
        self._queue = queue.Queue()
        self._jack_name = jack_name

        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

        AudioMixer.Factory.get().register(self.audio_mixer_on_notify)

    def audio_mixer_on_notify(self, event: AudioMixer.Event) -> None:
        """Handles notification DEFAULT_OUTPUT_CHANGED."""

        if event is None or not isinstance(event, AudioMixer.Event):
            return

        match event:
            case AudioMixer.Event.DEFAULT_OUTPUT_CHANGED:
                value = AudioMixer.Factory.get()._cfg.default_output
                if value != self._jack_name:
                    log.debug("Changing output value form '%s' to '%s'",
                              value, self._jack_name)
                self._jack_name = value
            case _:
                return

    def _worker(self):
        """The worker thread that plays and stops the audio files.

        Args:
            None:

        Returns:
            None:
        """

        log.info("Starting worker ...")

        dequeue_message_counter: int = 0
        process_message_counter: int = 0
        while True:
            dequeue_message_counter += 1

            try:

                # First, handle process termination requests.
                if self._do_cancel_item:

                    if self._process is not None and self._process.is_running:

                        pid = self._process.pid
                        log.debug(
                            "Cancelling currently playing item [%s] ...",
                            pid)

                        self._process.stop(force=True)
                        self._process = None

                        log.info(
                            "Cancelling currently playing item [%s] OK.",
                            pid)

                    self._do_cancel_item = False

                # Then check, if the whole worker shall be stopped.
                if self._do_cancel_worker.is_set():

                    log.info("Exiting worker ...")
                    break

                # Only then, skip if a process is still running.
                if self._process is not None and self._process.is_running:

                    if 0 == process_message_counter % 25:
                        process_message_counter += 1

                        log.debug(
                            "Process still running [%s] ...", self._process.pid)
                        continue

                # Otherwise, try to dequeue and play next item.
                if 0 == dequeue_message_counter % 25:
                    dequeue_message_counter = 0
                    log.debug("Trying to dequeue item ...")

                file, do_loop = self._queue.get(block=False)

                log.info(
                    "Trying to play '%s' [loop=%s] to '%s' ...",
                    file,
                    do_loop,
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
                if do_loop:
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
                # if do_loop:
                #     cmd.append(self._ECASOUND_OPTION_LOOP)
                self._process = Process.start(cmd)
                process_message_counter = 0

            except queue.Empty:

                # log.debug(
                #     "Queue empty. Sleeping [%sms] ...",
                #     self.WAIT_INTERVAL_MS)
                pass

            except Exception as ex:  # pylint: disable=W0718

                log.error(
                    "An exception occurred inside the worker thread: '%s'.",
                    ex,
                    exc_info=True)

            finally:
                time.sleep(self.WAIT_INTERVAL_MS/1000)

        log.info("Worker stopped.")

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

        self._do_cancel_worker.set()
        self._thread.join()

    def clear(self, do_stop_active_item: bool = False) -> None:
        """Clears the internal audio queue.

        Attributes:
            do_stop_active_item (bool): True, if the currently playing item
                shall be stopped (if there is one); false otherwise.
        Returns:
            None:
        """

        log.info("Clearing queue ...")

        with self._queue.mutex:
            self._queue.queue.clear()
            self._queue.all_tasks_done.notify_all()
            self._queue.unfinished_tasks = 0

        if not do_stop_active_item:
            return

        self.next()

    def next(self) -> None:
        """Skips playing the active item and skips to the next item in the
        queue, if there is one.

        Attributes:
            None:

        Returns:
            None:
        """

        log.info("Skipping to next item ...")

        self._do_cancel_item = True

    def enqueue(self, item: tuple[str, bool]) -> None:
        """Enqueues an item in the audio queue.

        Attributes:
            item (tuple[str, bool]): An item to enqueue into the audio player.
                `str` contains a full path to an audio file; `bool` is true if
                the audio shall be looped continously; false otherwise.

        Returns:
            None:
        """

        assert item
        assert isinstance(item, tuple) and \
            len(item) == 2 and \
            isinstance(item[0], str) and \
            isinstance(item[1], bool)

        log.debug("Trying to enqueue item '%s' [loop=%s]", item[0], item[1])

        self._queue.put(item)
