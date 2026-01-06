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
from ..public.audio import FileFormat, SampleRate
from ..public.mixer import ConnectionInfo
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

    _JACK_CAPTURE_NAME = "jack_capture"
    _JACK_CAPTURE_FULLNAME = f"/usr/bin/{_JACK_CAPTURE_NAME}"
    _JACK_OPT_VERBOSE = "--verbose"
    _JACK_OPT_DISABLE_CONSOLE = "--disable-console"
    _JACK_OPT_DAEMON = "--daemon"
    _JACK_OPT_JACK_TRANSPORT = "--jack-transport"
    _JACK_OPT_FILE_FORMAT = "--format"
    _JACK_OPT_FILE_FORMAT_VALUE = FileFormat.FLAC
    _JACK_OPT_BIT_DEPTH = "--bitdepth"
    _JACK_OPT_BIT_DEPTH_VALUE = "24"
    _JACK_OPT_CHANNEL_COUNT = "--channels"
    _JACK_OPT_PORT_NAME = "--port"

    _message_queue: MessageQueue
    _sync_root: threading.Lock
    _callbacks: list[Callable[[threading.Event], None]]
    _processes: list[Process]

    _recordings: list[list[FileName]]
    _recordings_lock: threading.Lock

    state: AudioRecorder.Event

    items: dict[str, list[FileName]]

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
                (IAudioRecorderMessage, SystemMessage.Shutdown)):
            return

        if isinstance(message, SystemMessage.Shutdown):

            log.info("%s: Stopping ...", type(message).__qualname__)
            is_deleted = self.stop()
            log.info("%s: Stopping result: %s", type(
                message).__qualname__, is_deleted)

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
            assert items and isinstance(items, dict)
            assert all(isinstance(e, str) for e in items)
            assert all(
                isinstance(e, list) and all(
                    isinstance(item, FileName)
                    for item in e) for e in items.values())

            def _worker_start():
                self.start(items)

            threading.Thread(target=_worker_start, daemon=True).start()

            return

        if isinstance(message, msgt.RecordingStopCommand):

            log.debug("RecordingStopCommand")

            def _worker_stop():
                self.stop()

            threading.Thread(target=_worker_stop, daemon=True).start()

            return

        if isinstance(message, msgt.DeleteLastRecordingCommand):

            log.debug("DeleteLastRecordingCommand")

            with self._recordings_lock:
                if self._recordings:
                    items = self._recordings.pop()
                else:
                    log.error("No recordings.")
                    self._message_queue.publish(
                        msgt.DeleteLastRecordingNotification(False))
                    return

            result = True
            log.debug("Try to delete last take ...")
            for item in items:
                log.debug("Try to delete last take ['%s'] ...", item.fullname)
                is_deleted = item.delete()
                result &= is_deleted
                if is_deleted:
                    log.info(
                        "Try to delete last take ['%s'] SUCCEEDED.",
                        item.fullname)
                else:
                    log.error(
                        "Try to delete last take ['%s'] FAILED.",
                        item.fullname)

            if result:
                log.info("Try to delete last take SUCCEEDED.")
            else:
                log.error("Try to delete last take FAILED.")
            self._message_queue.publish(
                msgt.DeleteLastRecordingNotification(result))

            return

        log.warning("Unrecognized message: '%s'", message.id)

    def __init__(self):

        if not AudioRecorder.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        log.debug("Initializing ...")

        self._message_queue = MessageQueue.Factory.get()
        self._sync_root = threading.Lock()
        self._callbacks = []
        self._processes = []
        self._recordings = []
        self._recordings_lock = threading.Lock()
        self.state = AudioRecorder.Event.STOPPED
        self.items = []
        self._cue_points_times = []

        self._message_queue.register(
            self._on_message,
            lambda e: isinstance(
                e, (msgt.RecordingStartCommand,
                    msgt.RecordingStopCommand,
                    msgt.RecordingCuePointCommand,
                    msgt.DeleteLastRecordingCommand,
                    SystemMessage.Shutdown)))

        log.info("Initializing OK.")

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

    # def start(self, items: list[str], jack_device_name: str) -> bool:
    def start(self, items: dict[str, list[FileName]]) -> bool:
        """Starts a recording."""

        assert items and isinstance(items, dict)
        assert all(isinstance(e, str) for e in items)
        assert all(
            isinstance(e, list) and all(
                isinstance(item, FileName)
                for item in e) for e in items.values())

        if self.state != AudioRecorder.Event.STOPPED:
            return False

        self.items = items

        mixbus = AudioMixer.Factory.get().mixbus
        self._processes.clear()

        all_port_names: dict[str, int] = {}
        for mixbus_device_name, filenames in items.items():

            mixbus_device = mixbus.get_device(mixbus_device_name)
            port_names = [e.name for e in mixbus_device.sources]
            log.debug("[%s] Setting up capture from these '%s' ports [%s] ...",
                      mixbus_device_name, len(port_names), port_names)

            self._set_state(AudioRecorder.Event.STARTING)
            log.debug("Starting recording ... [%s]", [
                e.fullname for e in filenames])

            for filename in filenames:
                cmd: list[str] = [
                    self._JACK_CAPTURE_FULLNAME,
                    self._JACK_OPT_VERBOSE,
                    self._JACK_OPT_DISABLE_CONSOLE,
                    self._JACK_OPT_DAEMON,
                    self._JACK_OPT_JACK_TRANSPORT,
                    self._JACK_OPT_FILE_FORMAT,
                    self._JACK_OPT_FILE_FORMAT_VALUE,
                    self._JACK_OPT_BIT_DEPTH,
                    self._JACK_OPT_BIT_DEPTH_VALUE,
                    self._JACK_OPT_CHANNEL_COUNT,
                ]
                cmd.append(len(port_names))
                for port_name in port_names:
                    cmd.append(self._JACK_OPT_PORT_NAME)
                    cmd.append(port_name)
                    all_port_names[port_name] = 1 + \
                        all_port_names.get(port_name, 0)
                cmd.append(filename.fullname)
                self._processes.append(
                    Process.start(cmd, wait_on_completion=False))

        with self._sync_root:
            self._cue_points_times.clear()
            self._cue_points_times.append(time.monotonic())

        for port_name, count in all_port_names.items():
            others: list[str] = []
            log.debug("Waiting for '%s' connections on port '%s' ...",
                      count, port_name)
            while True:
                info = ConnectionInfo(JackConnection.get_connections3())
                others = [e for e in info.get_connection_entries(
                    port_name) if e.startswith(self._JACK_CAPTURE_NAME)]

                log.debug("%s [%s]: Connections [%s]", port_name, count, others)
                if count <= len(others):
                    break
                time.sleep(0.25)

        JackTransport().start()

        for mixbus_device_name, filenames in items.items():
            # Add the list of filenames to the recordings stacks used to delete
            # last recordings.
            with self._recordings_lock:
                self._recordings.append(filenames)

            log.info("Starting recording OK. [%s]", [
                e.fullname for e in filenames])
        self._set_state(AudioRecorder.Event.STARTED)

        return True

    def stop(self) -> bool:
        """Stops a recording."""

        # DFTODO - adjust to process all filenames.

        if self.state != AudioRecorder.Event.STARTED:
            return False

        # Weird syntax ... but here, we flatten the all filenames into a
        # single list.
        filenames = [f for _, f in self.items.items() for f in f]

        self._set_state(AudioRecorder.Event.STOPPING)
        log.debug("Stopping recording ... [%s]", [
                  e.fullname for e in filenames])

        JackTransport().stop()
        # Here we use the time that is used by jack_capture to periodically
        # flush its buffers.
        time.sleep(4)

        for process in self._processes:
            log.debug("Waiting for process [%s] ...", process.pid)
            # DFTODO - why do not use here "stop" or expose wait in "Process"?
            return_code = process._popen.wait()
            log.info(
                "Waiting for process [%s] OK. [%s]", process.pid, return_code)

        log.info("Stopping recording OK. [%s]", [
            e.fullname for e in filenames])
        self._set_state(AudioRecorder.Event.STOPPED)

        self._processes.clear()

        # DFTODO - the following section needs heavy cleanup.
        # * Extract to function
        # * Do seekpoint / cue marker calculation only once.
        # * Use const for cmd line options.
        # * Rethink section locking.
        for f in filenames:

            # DFTODO - extract to function.
            _METAFLAC_FULLNAME = "/usr/bin/metaflac"  # pylint: disable=C0103

            filename = f.filename
            fullname = f.fullname
            sample_rate: int = SampleRate.R48000.value
            samples: list[int] = []
            lines: list[str] = []

            # DFTODO - why do we lock this section?
            with self._sync_root:

                start_offset = self._cue_points_times[0]
                convert = TimeConversion(start_offset, sample_rate)

                track_count = 1
                lines.append(f'FILE "{filename}" WAVE')

                for point in self._cue_points_times[1:]:

                    sample = convert.get_samples_aligned(point)
                    samples.append(sample)

                    lines.append(f"TRACK {track_count:02} AUDIO")
                    lines.append(
                        f"INDEX 01 {convert.to_cuesheet_string(point)}")
                    track_count += 1

                text = '\n'.join(lines)

            cmd = [
                _METAFLAC_FULLNAME,
                f'--set-tag="TITLE={filename}"',
                fullname
            ]
            log.debug("Setting title: [%s]", cmd)
            Process.communicate(cmd)

            cuesheet_fullname = f"/tmp/{filename}.cue"
            cmd = [
                _METAFLAC_FULLNAME,
                f"--import-cuesheet-from={cuesheet_fullname}",
                fullname
            ]
            log.debug("Setting cue points: [%s]", text)
            with open(cuesheet_fullname, 'w', encoding='utf-8') as file:
                file.write(text)

            log.debug("Setting cue points: [%s]", cmd)
            Process.communicate(cmd)

            cmd = [
                _METAFLAC_FULLNAME,
            ]
            for sample in samples:
                cmd.append(f"--add-seekpoint={sample}")
            cmd.append(fullname)
            log.debug("Setting seek points: [%s]", cmd)
            Process.communicate(cmd)

        return True
