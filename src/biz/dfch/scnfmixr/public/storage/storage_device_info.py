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

"""Module storage_device_info."""


from dataclasses import dataclass


from ...public.storage import BlockDeviceType


@dataclass(frozen=True)
class StorageDeviceInfo:
    """Storage device info.

    Attributes:
        name (str): The name of the device.
        full_name (str): The full path name of the device.
        type (str): The blockdevice type of the device.
        mount_point (str | None): The mount point or None.
    """

    name: str
    full_name: str
    type: BlockDeviceType
    mount_point: str | None = None
