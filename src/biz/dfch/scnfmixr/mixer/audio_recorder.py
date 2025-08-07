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
from ..public.storage import FileName
from ..public.system import MessageBase
from ..public.messages import IAudioRecorderMessage
from ..public.messages import AudioRecorder as msgt
from ..mixer import AudioMixer
from ..public.system.messages import SystemMessage
from ..system import MessageQueue

from .time_conversion import TimeConversion


__all__ = [
    "AudioRecorder",
]


class AudioRecorder:
    """The JACK audio recorder.

    Attributes:
    """

    _MAX_CUE_POINTS = 99

    _message_queue: MessageQueue
    _sync_root: threading.Lock
    _callbacks: list[Callable[[threading.Event], None]]
    _processes: list[Process]
    state: AudioRecorder.Event

    items: list[FileName]

    _cue_points_times: list[float]

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

        if isinstance(message, msgt.RecordingCuePointCommand):

            log.debug("RecordingCuePointCommand: '%s'", message.value)

            with self._sync_root:
                if self._MAX_CUE_POINTS <= len(self._cue_points_times):
                    return
                self._cue_points_times.append(message.value)

            return

        if isinstance(message, msgt.RecordingStartCommand):

            log.debug("RecordingStartCommand")

            cmd = cast(msgt.RecordingStartCommand, message)
            items = cmd.items
            jack_device = cmd.jack_device
            assert items and isinstance(items, list) and 1 <= len(items) <= 2
            assert isinstance(jack_device, str) and jack_device.strip()

            def _worker_start():
                self.start(items, jack_device)

            threading.Thread(target=_worker_start, daemon=True).start()

            return

        if isinstance(message, msgt.RecordingStopCommand):

            log.debug("RecordingStopCommand")

            def _worker_stop():
                self.stop()

            threading.Thread(target=_worker_stop, daemon=True).start()

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
        self._cue_points_times = []

        self._message_queue.register(
            self._on_message,
            lambda e: isinstance(
                e, (msgt.RecordingStartCommand,
                    msgt.RecordingStopCommand,
                    msgt.RecordingCuePointCommand,
                    SystemMessage)))

        log.info("Initialising OK.")

    def _set_state(self, value: AudioRecorder.Event) -> None:
        """Private: Sets the private field _state of the audio mixer."""

        self.state = value

        # DFTODO - cleanup and find sth "better".
        match value:
            case AudioRecorder.Event.STARTING:
                self._message_queue.publish(
                    msgt.StartingNotification())
            case AudioRecorder.Event.STARTED:
                self._message_queue.publish(
                    msgt.StartedNotification())
            case AudioRecorder.Event.STOPPING:
                self._message_queue.publish(
                    msgt.StoppingNotification())
            case AudioRecorder.Event.STOPPED:
                self._message_queue.publish(
                    msgt.StoppedNotification())
            case AudioRecorder.Event.CONFIGURATION_CHANGING:
                self._message_queue.publish(
                    msgt.ConfigurationChangingNotification())
            case AudioRecorder.Event.CONFIGURATION_CHANGED:
                self._message_queue.publish(
                    msgt.ConfigurationChangedNotification())
            case AudioRecorder.Event.ERROR:
                self._message_queue.publish(
                    msgt.StateErrorMessage())

    def start(self, items: list[str], jack_device_name: str) -> bool:
        """Starts a recording."""

        assert items and isinstance(items, list) and 1 <= len(items) <= 2
        assert all(isinstance(e, FileName) for e in items)
        assert isinstance(jack_device_name, str) and jack_device_name.strip()

        if self.state != AudioRecorder.Event.STOPPED:
            return False

        mixbus = AudioMixer.Factory.get().mixbus
        jack_device = mixbus.get_device(jack_device_name)
        port_names = [e.name for e in jack_device.sources]
        log.debug("Setting up capture from these '%s' ports [%s] ...",
                  len(port_names), port_names)

        self.items = items

        self._set_state(AudioRecorder.Event.STARTING)
        log.debug("Starting recording ... [%s]", [
                  e.fullname for e in self.items])

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
                # "2",
                # "EX2-O:*",
                # "-p",
                # "MixBus:*",
                # "-p",
                # "MixBus:MX0:capture_1",
                # "-p",
                # "MixBus:MX0:capture_2",
                # item
            ]
            cmd.append(len(port_names))
            for port_name in port_names:
                cmd.append("-p")
                cmd.append(port_name)
            cmd.append(item)
            self._processes.append(Process.start(cmd, wait_on_completion=False))

        while not JackConnection.has_client_name("jack_capture"):
            time.sleep(0.25)

        JackTransport().start()
        with self._sync_root:
            self._cue_points_times.clear()
            self._cue_points_times.append(time.monotonic())

        log.info("Starting recording OK. [%s]", [
                 e.fullname for e in self.items])
        self._set_state(AudioRecorder.Event.STARTED)

        return True

    def stop(self) -> bool:
        """Stops a recording."""

        if self.state != AudioRecorder.Event.STARTED:
            return False

        self._set_state(AudioRecorder.Event.STOPPING)
        log.debug("Stopping recording ... [%s]", [
                  e.fullname for e in self.items])

        JackTransport().stop()
        time.sleep(3)

        for process in self._processes:
            log.debug("Waiting for process [%s] ...", process.pid)
            return_code = process._popen.wait()
            log.info(
                "Waiting for process [%s] OK. [%s]", process.pid, return_code)

        log.info("Stopping recording OK. [%s]", [
            e.fullname for e in self.items])
        self._set_state(AudioRecorder.Event.STOPPED)

        self._processes.clear()

        fileitem: FileName = self.items[0]
        filename = fileitem.filename
        sample_rate: int = 48000
        samples: list[int] = []
        lines: list[str] = []

        with self._sync_root:

            start_offset = self._cue_points_times[0]
            convert = TimeConversion(start_offset, sample_rate)

            track_count = 1
            lines.append(f'FILE "{filename}" WAVE')

            for point in self._cue_points_times[1:]:

                sample = convert.get_samples_aligned(point)
                samples.append(sample)

                lines.append(f"TRACK {track_count:02} AUDIO")
                lines.append(f"INDEX 01 {convert.to_cuesheet_string(point)}")
                track_count += 1

            text = '\n'.join(lines)

        cmd = [
            "/usr/bin/metaflac",
            f'--set-tag="TITLE={filename}"',
            fileitem.fullname
        ]
        log.debug("Setting title: [%s]", cmd)
        Process.communicate(cmd)

        cuesheet_fullname = f"/tmp/{filename}.cue"
        cmd = [
            "/usr/bin/metaflac",
            f"--import-cuesheet-from={cuesheet_fullname}",
            fileitem.fullname
        ]
        log.debug("Setting cue points: [%s]", text)
        with open(cuesheet_fullname, 'w', encoding='utf-8') as file:
            file.write(text)

        log.debug("Setting cue points: [%s]", cmd)
        Process.communicate(cmd)

        cmd = [
            "/usr/bin/metaflac",
        ]
        for sample in samples:
            cmd.append(f"--add-seekpoint={sample}")
        cmd.append(fileitem.fullname)
        log.debug("Setting seek points: [%s]", cmd)
        Process.communicate(cmd)

        return True
