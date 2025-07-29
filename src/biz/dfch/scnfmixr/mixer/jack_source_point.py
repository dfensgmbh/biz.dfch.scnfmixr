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

"""Module jack_source_point."""

from __future__ import annotations
from typing import TYPE_CHECKING

from ..public.mixer import (
    ConnectionPolicy,
    IConnectableSink,
)
from .source_point import SourcePoint
if TYPE_CHECKING:
    from .jack_signal_manager import JackSignalManager


__all__ = [
    "JackSourcePoint",
]


class JackSourcePoint(
        SourcePoint,
):
    """Represents a JACK ALSA source point."""

    _mgr: "JackSignalManager"

    def __init__(self, name, info):
        super().__init__(name, info)

        from .jack_signal_manager import JackSignalManager\
            # pylint: disable=C0415

        self._mgr = JackSignalManager.Factory.get()

    def connect_to(self, other, policy=ConnectionPolicy.DEFAULT):

        assert isinstance(other, IConnectableSink)
        if ConnectionPolicy.DEFAULT == policy:
            policy = ConnectionPolicy.MONO

        result = self._mgr.get_signal_paths(
            self, other, policy)

        assert isinstance(result, list) and 1 == len(result), result

        _, path = result[0]
        path.acquire()

        return result
