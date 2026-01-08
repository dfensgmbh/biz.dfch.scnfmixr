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

"""Package device_operations."""

import os
import re

from biz.dfch.logging import log
from biz.dfch.asyn import Process
from text import TextUtils

from ...public.storage import StorageDeviceInfo
from ...public.storage import FileName


__all__ = [
    "DeviceOperations",
]


class DeviceOperations:
    """Provides operations on a storage device.

    Attributes:
        is_mounted (bool): Determines wether the device is mounted.
    """

    _TRAILING_DIGITS = r'\d+$'
    _EMPTY = ''
    _SPACE = ' '

    _SUDO_FULLNAME = "/usr/bin/sudo"
    _UDISKSCTL_FULLNAME = "/usr/bin/udisksctl"
    _UDISKSCTL_CMD_UNMOUNT = "unmount"
    _UDISKSCTL_CMD_POWEROFF = "power-off"
    _UDISKSCTL_OPT_BLOCK_DEVICE = "-b"

    _WIPEFS_FULLNAME = "/usr/sbin/wipefs"
    _WIPEFS_OPT_ALL = "--all"
    _WIPEFS_OPT_FORCE = "--force"

    _PARTED_FULLNAME = "parted"
    _PARTED_CMD_MKLABEL = "mklabel"
    _PARTED_CMD_MKLABEL_MSDOS = "msdos"
    _PARTED_OPT_A = "-a"
    _PARTED_OPT_A_VALUE = "optimal"
    _PARTED_CMD_MKPART = "mkpart"
    _PARTED_CMD_MKPART_PRIMARY = "primary"
    _PARTED_CMD_MKPART_PRIMARY_START = "0%"
    _PARTED_CMD_MKPART_PRIMARY_END = "100%"
    _PARTED_STDERR_INFO_PREFIX = "Information"

    _MKFS_EXFAT_FULLNAME = "/usr/sbin/mkfs.exfat"
    _MKFS_EXFAT_OPT_NAME = "-L"
    _MKFS_EXFAT_OPT_BLOCKSIZE = "-b"
    _MKFS_EXFAT_OPT_BLOCKSIZE_VALUE = "4096"

    _PROC_MOUNT_FULLNAME = "/proc/mounts"

    _MOUNT_FULLNAME = "/usr/bin/mount"
    _MOUNT_OPTION_OWNER = "-o"
    _MOUNT_OPTION_OWNER_VALUE = "uid=%s,gid=%s"
    _MOUNT_OPTION_OWNER_VALUE = (
        "rw,noexec,nosuid,nodev,"
        "uid=%s,gid=%s,"
        "fmask=0022,dmask=0022,iocharset=utf8,"
        "errors=remount-ro"
    )
    _UMOUNT_FULLNAME = "/usr/bin/umount"

    _MESSAGE_OK_2 = "'%s' OK: [%s]"
    _MESSAGE_FAILED_2 = "'%s' FAILED: [%s]"
    _MESSAGE_RETURNED_2 = "'%s' RETURNED: [%s]"

    _uid: str
    _gid: str

    _device_info: StorageDeviceInfo

    def __init__(self, value: StorageDeviceInfo):
        """Initializes an instance of the object.

        Args:
            value (StorageDeviceInfo): The storage device to manipulate.
        """

        assert value and isinstance(value, StorageDeviceInfo)

        self._device_info = value
        self._uid = os.getuid()  # pylint: disable=E1101
        self._gid = os.getgid()  # pylint: disable=E1101

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
            self._MOUNT_OPTION_OWNER,
            self._MOUNT_OPTION_OWNER_VALUE % (self._uid, self._gid),
            self._device_info.full_name,
            self._device_info.mount_point,
        ]

        process = Process.start(cmd, wait_on_completion=True)

        return 0 == process.exit_code

    def clean(self) -> bool:
        """Cleans a device.

        Returns:
            bool: True, if operation was successful; false, otherwise.
        """

        if not self.is_mounted:
            log.error("The device '%s' is not mounted.",
                      self._device_info.full_name)
            return False

        log.debug("Try to retrieve files from '%s' [%s] ...",
                  self._device_info.full_name,
                  self._device_info.mount_point)

        for name in os.listdir(self._device_info.mount_point):
            full_name = os.path.join(self._device_info.mount_point, name)
            if not os.path.isfile(full_name):
                continue

            is_valid = FileName.is_valid_filename(name)
            if not is_valid:
                continue
            log.debug("Found valid file '%s'.", full_name)

            filename = FileName.from_full_name(full_name)
            log.debug("Try to clean '%s' ...", filename.fullname)

            result = filename.delete()
            if result:
                log.info("Try to clean '%s' SUCCEEDED.", full_name)
            else:
                log.error("Try to clean '%s' FAILED.", full_name)

        return True

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

    def initialize_disk(self, name: str) -> bool:
        """Removes all partitions and creates a new single partition with ExFAT
        file system."""

        assert isinstance(name, str) and name.strip()

        block_device = re.sub(self._TRAILING_DIGITS,
                              self._EMPTY, self._device_info.full_name)

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._WIPEFS_FULLNAME,
            self._WIPEFS_OPT_ALL,
            self._WIPEFS_OPT_FORCE,
            block_device,
        ]

        stdout, stderr = Process.communicate(cmd)
        if 0 < len(stderr):
            log.warning(self._MESSAGE_FAILED_2, self._SPACE.join(cmd), stderr)
            return False
        if 0 < len(stdout):
            log.debug(self._MESSAGE_OK_2, self._SPACE.join(cmd), stdout)

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._PARTED_FULLNAME,
            block_device,
            self._PARTED_CMD_MKLABEL,
            self._PARTED_CMD_MKLABEL_MSDOS,
        ]

        stdout, stderr = Process.communicate(cmd)
        if 0 < len(stderr):
            log.warning(self._MESSAGE_RETURNED_2, self._SPACE.join(cmd), stderr)
            if not stderr[0].startswith(self._PARTED_STDERR_INFO_PREFIX):
                return False
        if 0 < len(stdout):
            log.debug(self._MESSAGE_OK_2, self._SPACE.join(cmd), stdout)

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._PARTED_FULLNAME,
            self._PARTED_OPT_A,
            self._PARTED_OPT_A_VALUE,
            block_device,
            self._PARTED_CMD_MKPART,
            self._PARTED_CMD_MKPART_PRIMARY,
            self._PARTED_CMD_MKPART_PRIMARY_START,
            self._PARTED_CMD_MKPART_PRIMARY_END,
        ]

        stdout, stderr = Process.communicate(cmd)
        if 0 < len(stderr):
            log.warning(self._MESSAGE_RETURNED_2, self._SPACE.join(cmd), stderr)
            if not stderr[0].startswith(self._PARTED_STDERR_INFO_PREFIX):
                return False
        if 0 < len(stdout):
            log.debug(self._MESSAGE_OK_2, self._SPACE.join(cmd), stdout)

        if self._device_info.full_name[-1].isdigit():
            partition_device = self._device_info.full_name
        else:
            partition_device = f"{self._device_info.full_name}1"

        cmd: list[str] = [
            self._SUDO_FULLNAME,
            self._MKFS_EXFAT_FULLNAME,
            self._MKFS_EXFAT_OPT_NAME,
            name,
            self._MKFS_EXFAT_OPT_BLOCKSIZE,
            self._MKFS_EXFAT_OPT_BLOCKSIZE_VALUE,
            partition_device,
        ]

        stdout, stderr = Process.communicate(cmd)
        if 0 < len(stderr):
            log.warning(self._MESSAGE_FAILED_2, self._SPACE.join(cmd), stderr)
            return False
        if 0 < len(stdout):
            log.debug(self._MESSAGE_OK_2, self._SPACE.join(cmd), stdout)

        return True
