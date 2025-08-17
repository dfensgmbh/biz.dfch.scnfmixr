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

"""Module starting_recording_mx0."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...system import FuncExecutor
from ...mixer.audio_recorder import AudioRecorder
from ...public.messages import AudioRecorder as msgt
from ...public.storage import FileName
from ...public.system import SystemTime
from ...public.mixer import MixbusDevice
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..transition_event import TransitionEvent


class StartingRecording(TransitionBase):
    """Starts a recording."""

    _devices: list[MixbusDevice] = []

    def __init__(
            self,
            event: str,
            target: StateBase,
            devices: list[MixbusDevice]):

        assert event and event.strip()
        assert target
        assert isinstance(devices, list)
        assert all(isinstance(e, MixbusDevice) for e in devices)

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.STARTING_RECORDING_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.STARTING_RECORDING_LEAVE, False),
            target_state=target)

        self._devices = devices

    def invoke(self, _):

        app_ctx = ApplicationContext.Factory.get()
        base_name = app_ctx.date_time_name_input.get_name()
        now = SystemTime.Factory.get().now()

        items: dict[str, list[FileName]] = {}

        AudioRecorder.Factory.get()

        for mixbus_device in self._devices:

            files: list[FileName] = []

            suffix = mixbus_device.name
            for device, device_info in \
                    app_ctx.storage_configuration_map.items():

                file = FileName(
                    path_name=device_info.mount_point,
                    base_name=base_name,
                    dt=now,
                    suffix=suffix
                )

                log.debug("[%s] Filename '%s' [path: %s] [file: %s]",
                          device.name,
                          file.fullname,
                          file.direxists,
                          file.exists)

                if file.direxists and not file.exists:
                    files.append(file)

            if 0 == len(files):
                log.error("No storage devices detected. Cannot record.")
                return False

            items[mixbus_device.value] = files

        log.debug("Waiting for recording to start ... [%s]", items)

        with FuncExecutor(
            lambda _: True,
            lambda e: isinstance(e, msgt.StartedNotification)
        ) as sync:
            result = sync.invoke(
                msgt.RecordingStartCommand(items))

        if result:
            log.info("Waiting for recording to start OK.")
        else:
            log.error("Waiting for recording to start FAILED.")

        return result
