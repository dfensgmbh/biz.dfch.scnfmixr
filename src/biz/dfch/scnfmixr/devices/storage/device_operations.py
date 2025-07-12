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

"""Package device_operations."""

from biz.dfch.asyn import Process
from text import TextUtils
from ...public.storage import StorageDeviceInfo

__all__ = [
    "DeviceOperations",
]


class DeviceOperations:
    """Provides operations on a storage device.

    Attributes:
        is_mounted (bool): Determines wether the device is mounted.
    """

    _SUDO_FULLNAME = "/usr/bin/sudo"
    _UDISKSCTL_FULLNAME = "/usr/bin/udisksctl"
    _UDISKSCTL_CMD_UNMOUNT = "unmount"
    _UDISKSCTL_CMD_POWEROFF = "power-off"
    _UDISKSCTL_OPT_BLOCK_DEVICE = "-b"

    _PROC_MOUNT_FULLNAME = "/proc/mounts"

    _MOUNT_FULLNAME = "/usr/bin/mount"
    _UMOUNT_FULLNAME = "/usr/bin/umount"

    _device_info: StorageDeviceInfo

    def __init__(self, value: StorageDeviceInfo):
        """Initialises an instance of the object.

        Args:
            value (StorageDeviceInfo): The storage device to manipulate.
        """

        assert value and isinstance(value, StorageDeviceInfo)

        self._device_info = value

    @property
    def is_mounted(self) -> bool:
        """Determines wether the device is mounted.

        Returns:
            bool: True, if the device is mounted; false, otherwise.
        """

        text = TextUtils().read_all_lines(self._PROC_MOUNT_FULLNAME)

        return any(e.startswith(self._device_info.full_name) for e in text)

    def mount(self) -> bool:
        """Mounts a device.

        Returns:
            bool: True, if operation was successful; false, otherwise.
        """

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._MOUNT_FULLNAME,
            self._device_info.full_name,
            self._device_info.mount_point,
        ]

        process = Process.start(cmd, wait_on_completion=True)

        return 0 == process.exit_code

    def unmount(self) -> bool:
        """Unmounts a device.

        Returns:
            bool: True, if operation was successful; false, otherwise.
        """

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._UDISKSCTL_FULLNAME,
            self._UDISKSCTL_CMD_UNMOUNT,
            self._UDISKSCTL_OPT_BLOCK_DEVICE,
            self._device_info.full_name,
        ]

        process = Process.start(cmd, wait_on_completion=True)

        return 0 == process.exit_code

    def poweroff(self) -> bool:
        """Powers off an unmounted device.

        Returns:
            bool: True, if operation was successful; false, otherwise.
        """

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._UDISKSCTL_FULLNAME,
            self._UDISKSCTL_CMD_POWEROFF,
            self._UDISKSCTL_OPT_BLOCK_DEVICE,
            self._device_info.full_name,
        ]

        process = Process.start(cmd, wait_on_completion=True)

        return 0 == process.exit_code

    def format(self) -> bool:
        """Formats a partition."""

        raise NotImplementedError("Not yet implemented.")

    def initialise_disk(self) -> bool:
        """Removes all partitions and creates a new single partition with ExFAT
        file system."""

        raise NotImplementedError("Not yet implemented.")
