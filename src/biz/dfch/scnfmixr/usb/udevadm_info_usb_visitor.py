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

"""Module udevadm_info_usb_all_visitor."""

from dataclasses import dataclass

from text import MultiLineTextParser
from text import MultiLineTextParserContext
from text import MultiLineTextParserMap

from ..text.visitor_base import VisitorBase

__all__ = [
    "UdevadmInfoVisitor",
]


class UdevadmInfoVisitor(VisitorBase):
    """Visitor for parsing `udevadm info -a --name /dev/X`."""

    @dataclass(frozen=True)
    class Data:
        """Parsed USB device data.

        Attributes:
            usb_id (str): The USB id of the device.
            device_type (str): The device type, such as usb-storage.
            name0 (str): The name of the device.
            device0_path (str): The path of the device.
            name1 (str): The parent name of the device.
            device1_path (str): The parent path of the device.
        """

        usb_id: str
        device_type: str
        name0: str
        device0_path: str
        name1: str
        device1_path: str

    _parser: MultiLineTextParser
    _dic: MultiLineTextParserMap
    _data: dict[str, str]
    _parent_hierarchy: int

    def __init__(self):

        self._dic = {
            "looking at device '": self._process_device,
            "looking at parent device '": self._process_parent_device,
            "KERNEL==": self._process_kernel,
            "KERNELS==": self._process_kernels,
            "SUBSYSTEMS==": self._process_subsystems,
            "DRIVERS==": self._process_drivers,
        }

        self._data = {}
        self._parent_hierarchy = 0
        self._parser = MultiLineTextParser(" ", 2, self._dic, None)

    def get_result(self):
        """Returns parsed result."""

        return UdevadmInfoVisitor.Data(
            usb_id=self._data["usb_id"],
            device_type=self._data["device_type"],
            name0=self._data["name0"],
            name1=self._data["name1"],
            device0_path=self._data["device0_path"],
            device1_path=self._data["device1_path"],
        )

    def _process_device(self, ctx: MultiLineTextParserContext) -> bool:
        """Process device path."""

        value = ctx.text.removeprefix(ctx.keyword).strip("':")
        self._data["device0_path"] = value

        return True

    def _process_parent_device(self, ctx: MultiLineTextParserContext) -> bool:
        """Process parent device path."""

        self._parent_hierarchy += 1
        if 1 == self._parent_hierarchy:

            value = ctx.text.removeprefix(ctx.keyword).strip('"')
            self._data["device1_path"] = value

        return True

    def _process_kernel(self, ctx: MultiLineTextParserContext) -> bool:
        """Process KERNEL."""

        value = ctx.text.removeprefix(ctx.keyword).strip('"')
        self._data["name0"] = value
        return True

    def _process_kernels(self, ctx: MultiLineTextParserContext) -> bool:
        """Process KERNELS."""

        if 1 == self._parent_hierarchy:
            self._data["name1"] = ctx.text.removeprefix(ctx.keyword).strip('"')

        value = ctx.text.removeprefix(ctx.keyword).strip('"')
        self._data["last_kernels"] = value

        return True

    def _process_subsystems(self, ctx: MultiLineTextParserContext) -> bool:
        """Process SUBSYSTEMS."""

        value = ctx.text.removeprefix(ctx.keyword).strip('"')
        self._data["last_subsystems"] = value

        return True

    def _process_drivers(self, ctx: MultiLineTextParserContext) -> bool:
        """Process DRIVERS."""

        value = ctx.text.removeprefix(ctx.keyword).strip('"')
        self._data["last_drivers"] = value

        result = True
        if (
            "usb" != self._data["last_drivers"]
            and "usb" == self._data["last_subsystems"]
        ):

            self._data["device_type"] = self._data["last_drivers"]
            result = True

        elif (
            "usb" == self._data["last_drivers"]
                and "usb" == self._data["last_subsystems"]
        ):

            self._data["usb_id"] = self._data["last_kernels"]
            result = False

        del self._data["last_drivers"]
        del self._data["last_kernels"]
        del self._data["last_subsystems"]
        return result

    def visit(self, value, _=False):

        self._data.clear()

        self._parser.parse(value)
