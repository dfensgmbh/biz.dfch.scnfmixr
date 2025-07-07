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
