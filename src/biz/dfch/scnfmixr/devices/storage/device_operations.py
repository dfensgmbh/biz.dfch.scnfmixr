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

__all__ = [
    "DeviceOperations",
]


class DeviceOperations():
    """Provides operations on a storage device."""

    _SUDO_FULLNAME = "/usr/bin/sudo"
    _MOUNT_FULLNAME = "/usr/bin/mount"
    _UMOUNT_FULLNAME = "/usr/bin/umount"

    @staticmethod
    def mount(device: str, mount_point: str) -> bool:
        """Mounts a partition.

        Args:
            device (str): Device to mount.
            mount_point (str): Target directory to mount into.

        Returns:
            bool: True, if operation was successful. False, otherwise.
        """

        assert device and device.strip()
        assert mount_point and mount_point.strip()

        cmd: list[str] = [
            DeviceOperations._SUDO_FULLNAME,
            DeviceOperations._MOUNT_FULLNAME,
            device,
            mount_point,
        ]

        process = Process.start(cmd, wait_on_completion=True)

        return 0 == process.exit_code

    @staticmethod
    def unmount(mount_point: str) -> bool:
        """Unmounts a partition.

        Args:
            mount_point (str): Target directory to unmount from.

        Returns:
            bool: True, if operation was successful. False, otherwise.
        """

        assert mount_point and mount_point.strip()

        cmd: list[str] = [
            DeviceOperations._SUDO_FULLNAME,
            DeviceOperations._UMOUNT_FULLNAME,
            mount_point,
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
