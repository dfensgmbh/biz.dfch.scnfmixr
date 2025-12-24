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

"""Module input_event_device_visitor."""

from text import MultiLineTextParserContext
from biz.dfch.logging import log
from .input_event_device_info import InputEventDeviceInfo


class InputEventDeviceVisitor:
    """Visitor class for extracting HID related udevadm information."""

    _path: str
    _name: str
    _input: bool

    def __init__(self):
        self._path = None
        self._name = None
        self._input = False

    def process_devpath(self, ctx: MultiLineTextParserContext) -> bool:
        """Process DEVPATH."""

        log.debug("[process_devpath] %s: '%s'", ctx.keyword, ctx.text)
        self._path = ctx.text.removeprefix(ctx.keyword)
        return True

    def process_devname(self, ctx: MultiLineTextParserContext) -> bool:
        """Process DEVNAME."""

        log.debug("[process_devname] %s: '%s'", ctx.keyword, ctx.text)
        self._name = ctx.text.removeprefix(ctx.keyword)
        return True

    def process_id_input_keyboard(
            self, ctx: MultiLineTextParserContext) -> bool:
        """Process ID_INPUT_KEYBOARD."""

        log.debug("[process_id_input_keyboard] %s: '%s'", ctx.keyword, ctx.text)
        self._input = bool(int(ctx.text.removeprefix(ctx.keyword)))

        # Abort processing wwhen all parameters were found.
        if self._path and self._name and self._input:
            return False
        return True

    @property
    def result(self) -> InputEventDeviceInfo:
        """Returns the result of the visitor, if any.

        Returns:
            InputEventDeviceInfo: The extracted information.
        """
        return InputEventDeviceInfo(self._path, self._name, self._input)
