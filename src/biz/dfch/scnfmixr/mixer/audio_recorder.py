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

"""Module audio_recorder."""

from __future__ import annotations
from enum import Enum, auto
import time
import threading
from typing import (
    Callable,
    ClassVar,
    cast
)

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from ..jack_commands import (
    JackConnection,
    JackTransport,
)
from ..public.mixer import (
    IAudioRecorderMessage,
    MixerMessage
)
from ..public.system import MessageBase
from ..public.system.messages import SystemMessage
from ..system import MessageQueue


__all__ = [
    "AudioRecorder",
]


class AudioRecorder:
    """The JACK audio recorder.

    Attributes:
    """

    _message_queue: MessageQueue
    _sync_root: threading.Lock
    _callbacks: list[Callable[[threading.Event], None]]
    _processes: list[Process]
    state: AudioRecorder.Event

    items: list[str]

    class Event(Enum):
        """Notification events."""

        ERROR = auto()
        CONFIGURATION_CHANGING = auto()
        CONFIGURATION_CHANGED = auto()
        STARTING = auto()
        STARTED = auto()
        STOPPING = auto()
        STOPPED = auto()
        STATE_CHANGED = auto()

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AudioRecorder | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

        @staticmethod
        def get() -> AudioRecorder:
            """Gets the instance of the audio mixer."""

            if AudioRecorder.Factory.__instance is not None:
                return AudioRecorder.Factory.__instance

            with AudioRecorder.Factory._sync_root:

                if AudioRecorder.Factory.__instance is not None:
                    return AudioRecorder.Factory.__instance

                AudioRecorder.Factory.__instance = AudioRecorder()

            return AudioRecorder.Factory.__instance

    def _on_message(self, message: MessageBase) -> None:
        """Message handler."""

        assert message

        if not isinstance(
                message,
                (IAudioRecorderMessage, SystemMessage)):
            return

        if isinstance(message, SystemMessage.Shutdown):

            log.info("%s: Stopping ...", type(message).__qualname__)
            result = self.stop()
            log.info("%s: Stopping result: %s", type(
                message).__qualname__, result)

            return

        if isinstance(message, MixerMessage.Recorder.RecordingStartCommand):

            log.debug("RecordingStartCommand")

            cmd = cast(MixerMessage.Recorder.RecordingStartCommand, message)
            items = cmd.items
            assert items and isinstance(items, list) and 1 <= len(items) <= 2

            self.start(items)

            return

        if isinstance(message, MixerMessage.Recorder.RecordingStopCommand):

            log.debug("RecordingStopCommand")

            self.stop()

            return

    def __init__(self):

        if not AudioRecorder.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initialising ...")

        self._message_queue = MessageQueue.Factory.get()
        self._sync_root = threading.Lock()
        self._callbacks = []
        self._processes = []
        self.state = AudioRecorder.Event.STOPPED
        self.items = []

        self._message_queue.register(self._on_message)

        log.info("Initialising OK.")

    def _set_state(self, value: AudioRecorder.Event) -> None:
        """Private: Sets the private field _state of the audio mixer."""

        self.state = value

        # DFTODO - cleanup and find sth "better".
        match value:
            case AudioRecorder.Event.STARTING:
                self._message_queue.publish(
                    MixerMessage.Recorder.StartingMessage())
            case AudioRecorder.Event.STARTED:
                self._message_queue.publish(
                    MixerMessage.Recorder.StartedMessage())
            case AudioRecorder.Event.STOPPING:
                self._message_queue.publish(
                    MixerMessage.Recorder.StoppingMessage())
            case AudioRecorder.Event.STOPPED:
                self._message_queue.publish(
                    MixerMessage.Recorder.StoppedMessage())
            case AudioRecorder.Event.CONFIGURATION_CHANGING:
                self._message_queue.publish(
                    MixerMessage.Recorder.ConfigurationChanging())
            case AudioRecorder.Event.CONFIGURATION_CHANGED:
                self._message_queue.publish(
                    MixerMessage.Recorder.ConfigurationChanged())
            case AudioRecorder.Event.ERROR:
                self._message_queue.publish(
                    MixerMessage.Recorder.StateErrorMessage())

    def start(self, items: list[str]) -> bool:
        """Starts a recording."""

        assert items and isinstance(items, list) and 1 <= len(items) <= 2

        if self.state != AudioRecorder.Event.STOPPED:
            return False

        self.items = items

        self._set_state(AudioRecorder.Event.STARTING)
        log.debug("Starting recording ... [%s]", self.items)

        self._processes.clear()
        for item in items:
            cmd: list[str] = [
                "/usr/bin/jack_capture",
                # "-V",
                "-dc",
                "--daemon",
                "-jt",
                "-f",
                "flac",
                "-b",
                "24",
                "-c",
                "2",
                # "-jt",
                # "-p",
                # "EX2-O:*",
                "-p",
                "EX2-O:playback_1",
                "-p",
                "EX2-O:playback_2",
                item
            ]
            self._processes.append(Process.start(cmd, wait_on_completion=False))

        while not JackConnection.has_client_name("jack_capture"):
            time.sleep(0.25)

        JackTransport().start()

        log.info("Starting recording OK. [%s]", self.items)
        self._set_state(AudioRecorder.Event.STARTED)

        return True

    def stop(self) -> bool:
        """Stops a recording."""

        if self.state != AudioRecorder.Event.STARTED:
            return False

        self._set_state(AudioRecorder.Event.STOPPING)
        log.debug("Stopping recording ... [%s]", self.items)

        JackTransport().stop()
        time.sleep(3)

        for process in self._processes:
            log.debug("Waiting for process [%s] ...", process.pid)
            return_code = process._popen.wait()
            log.info(
                "Waiting for process [%s] OK. [%s]", process.pid, return_code)

        log.info("Stopping recording OK. [%s]", self.items)
        self._set_state(AudioRecorder.Event.STOPPED)

        self._processes.clear()

        return True
