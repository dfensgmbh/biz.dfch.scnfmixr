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

from dataclasses import dataclass

__all__ = [
    "UsbDeviceInfo",
]


@dataclass(frozen=True)
class UsbDeviceInfo:
    """Contains information about a USB device.

    Attributes:
        manufacturer (str): The manfacturer name of the device.
        product (str): The product name of the device.
        version (str | None): The version of the device.
        id_vendor (str): The USB vendor id ('abcd').
        id_product (str): The USB product id ('1234').
        busnum (str): The USB bus number.
        devnum (str): The USB device number (increments between reconnects per
            bus).
    """

    manufacturer: str
    product: str
    version: str | None
    id_vendor: str
    id_product: str
    busnum: int
    devnum: int
