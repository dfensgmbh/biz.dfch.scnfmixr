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
