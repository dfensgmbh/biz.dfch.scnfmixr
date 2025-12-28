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

"""Module mix_bus."""

from threading import Lock

from biz.dfch.logging import log

from ..public.mixer import IConnectableDevice
from ..public.mixer import IConnectableSourcePoint
from ..public.mixer import IConnectableSinkPoint


class Mixbus():
    """Sets up the mix bus. **WIP**."""

    _sync_root = Lock
    _devices: list[IConnectableDevice]

    def __init__(self):

        self._sync_root = Lock()
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

        log.info("Starting OK.")

        return True

    def stop(self) -> None:
        """Stops the bus."""

        log.debug("Stopping ...")

        for device in self.devices:
            log.debug("Releasing device '%s' ...", device.name)
            device.release()
            log.info("Releasing device '%s' OK.", device.name)

        log.info("Stopping OK.")
