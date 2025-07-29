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

"""Module mix_bus."""

from threading import Lock

from biz.dfch.asyn import Process
from biz.dfch.logging import log

from ..public.mixer import IConnectableDevice
from ..public.mixer import IConnectableSourcePoint
from ..public.mixer import IConnectableSinkPoint


class Mixbus():
    """Sets up the mix bus. **WIP**."""

    _sync_root = Lock
    _process: Process | None
    _devices: list[IConnectableDevice]

    def __init__(self):

        self._sync_root = Lock()
        self._process = None
        self._devices = []

    @property
    def devices(self) -> list[IConnectableDevice]:
        """The iterable device list."""

        with self._sync_root:
            result = list(self._devices)

        return result

    @property
    def sources(self) -> list[IConnectableSourcePoint]:
        """Returns a list of source points."""

        result: list[IConnectableSourcePoint] = []

        with self._sync_root:
            for device in self._devices:
                result.extend([e for e in device.points if e.is_source])

        return result

    @property
    def sinks(self) -> list[IConnectableSinkPoint]:
        """Returns a list of sink points."""

        result: list[IConnectableSinkPoint] = []

        with self._sync_root:
            for device in self._devices:
                result.extend([e for e in device.points if e.is_sink])

        return result

    def add_device(self, item: IConnectableDevice) -> bool:
        """Adds a device to the device list.

        Args:
            item (IConnectableDevice): The device to add.

        Returns:
            bool: True, if the device was added; false, if the device was
                already added.
        """

        assert isinstance(item, IConnectableDevice)

        log.debug("Adding device '%s' ...", item.name)

        with self._sync_root:

            result = any(e is item and e.name == item.name
                         for e in self._devices)

            if result:
                log.warning("Adding device '%s' FAILED. Item already in list.",
                            item.name)
                return False

            self._devices.append(item)

            log.info("Adding device '%s' OK.", item.name)

            return True

    def remove_device(self, value: str) -> bool:
        """Removes a devices from the list.

        Returns:
            bool: True, if the device was removed; false, if the device could
                not be removed or was not in the list.
        """

        assert isinstance(value, str) and value.strip()

        log.debug("Removing device '%s' ...", value)

        with self._sync_root:

            result = next((e for e in self._devices if e.name == value), None)

            if result is not None:
                log.warning("Removing device '%s' FAILED. Item not in list.",
                            value)
                return False

            self._devices.remove(result)

            log.debug("Removing device '%s' OK.", value)

            return True

    def get_device(self, value: str) -> IConnectableDevice | None:
        """Retrieves a device from the device list."""

        log.debug("Getting device '%s' ...", value)

        with self._sync_root:

            result = next((e for e in self._devices if e.name == value), None)

            if result is None:
                log.warning("Getting device '%s' FAILED. Item not in list.",
                            value)
                return None

            log.debug("Getting device '%s' OK.", value)

            return result

    def start(self) -> bool:
        """Starts the bus."""

        log.debug("Starting ...")

        if self._process is not None:
            if self._process.is_running:
                log.warning(
                    "Starting FAILED. Process running [%s].",
                    self._process.pid)
            else:
                log.error(
                    "Starting FAILED. Process not None [%s].",
                    self._process.pid)

            return False

        # cmd = [
        #     'ecasound', '-r:80', '-B:rt',

        #     '-G:jack,MixBus,notransport',

        #     '-a:LCL-I-DRY', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,LCL-I-DRY-I', '-o:jack,,LCL-I-DRY-O',

        #     '-a:EX1-I-DRY', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,EX1-I-DRY-I', '-o:jack,,EX1-I-DRY-O',

        #     '-a:EX2-I-DRY', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,EX2-I-DRY-I', '-o:jack,,EX2-I-DRY-O',

        #     '-a:LCL-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
        #     '-i:jack,,LCL-I-WET-I', '-o:jack,,LCL-I-WET-O',

        #     '-a:EX1-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
        #     '-i:jack,,EX1-I-WET-I', '-o:jack,,EX1-I-WET-O',

        #     '-a:EX2-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
        #     '-i:jack,,EX2-I-WET-I', '-o:jack,,EX2-I-WET-O',

        #     '-a:MX0', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,MX0-I', '-o:jack,,MX0-O',

        #     '-a:MX1', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,MX1-I', '-o:jack,,MX1-O',

        #     '-a:MX2', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,MX2-I', '-o:jack,,MX2-O',

        #     '-a:MX3', '-f:f32_le,2,48000', '-efh:80',
        #     '-i:jack,,MX3-I', '-o:jack,,MX3-O',

        #     '-a:MX4', '-f:f32_le,12,48000', '-efh:80',
        #     '-i:jack,,MX4-I', '-o:jack,,MX4-O',
        # ]

        # self._process = Process.start(
        #     cmd, wait_on_completion=False,
        #     capture_stdout=True,
        #     capture_stderr=True)

        # log.debug("exit_code '%s'", self._process.exit_code)
        # log.debug("stdout '%s'", self._process.stdout)
        # log.debug("stderr '%s'", self._process.stderr)

        # while True:

        #     result = JackConnection.get_client_names()
        #     log.debug("Current JACK clients: [%s]", result)

        #     if "MixBus" in result:
        #         break

        #     time.sleep(0.1)

        # # Connect DRY to WET in stereo
        # JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:LCL-I-WET-I_1")
        # JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:LCL-I-WET-I_2")
        # JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:EX1-I-WET-I_1")
        # JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:EX1-I-WET-I_2")
        # JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:EX2-I-WET-I_1")
        # JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:EX2-I-WET-I_2")

        # # Setup mix-minus DRY for busses for LCL, EX1, EX2 on MX0, MX1, MX2.
        # JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX0-I_1")
        # JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX0-I_2")
        # JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX0-I_1")
        # JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX0-I_2")

        # JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX1-I_1")
        # JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX1-I_2")
        # JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX1-I_1")
        # JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX1-I_2")

        # JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX2-I_1")
        # JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX2-I_2")
        # JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX2-I_1")
        # JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX2-I_2")

        # # Setup stereo master mix.
        # JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        # JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX3-I_2")
        # JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        # JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX3-I_2")
        # JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        # JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX3-I_2")

        # # Setup iso mix
        # JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX4-I_1")
        # JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX4-I_2")
        # JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX4-I_3")
        # JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX4-I_4")
        # JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX4-I_5")
        # JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX4-I_6")
        # JackPort("MixBus:LCL-I-WET-O_1").connect_to("MixBus:MX4-I_7")
        # JackPort("MixBus:LCL-I-WET-O_2").connect_to("MixBus:MX4-I_8")
        # JackPort("MixBus:EX1-I-WET-O_1").connect_to("MixBus:MX4-I_9")
        # JackPort("MixBus:EX1-I-WET-O_2").connect_to("MixBus:MX4-I_10")
        # JackPort("MixBus:EX2-I-WET-O_1").connect_to("MixBus:MX4-I_11")
        # JackPort("MixBus:EX2-I-WET-O_2").connect_to("MixBus:MX4-I_12")

        log.info("Starting OK.")

        return True

    def stop(self) -> None:
        """Stops the bus."""

        log.debug("Stopping ...")

        if self._process is None:
            log.warning("Stopping FAILED [None].")
            return

        result = self._process.stop(force=True)
        if not result:
            log.warning("Stopping FAILED [%s].", result)
            return

        self._process = None

        log.info("Stopping OK.")
