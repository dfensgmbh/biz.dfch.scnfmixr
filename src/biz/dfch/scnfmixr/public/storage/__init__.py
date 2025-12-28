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

"""Package storage."""

from __future__ import annotations

from .block_device_type import BlockDeviceType
from .file_name import FileName
from .mount_point import MountPoint
from .storage_device import StorageDevice
from .storage_device_info import StorageDeviceInfo
from .storage_device_map import StorageDeviceMap
from .storage_parameters import StorageParameters

__all__ = [
    "BlockDeviceType",
    "FileName",
    "MountPoint",
    "StorageDevice",
    "StorageDeviceInfo",
    "StorageDeviceMap",
    "StorageParameters",
]
