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

"""Module schescheduling_infoduling."""

import resource
from dataclasses import dataclass

__all__ = [
    "SchedulingInfo",
]


@dataclass(frozen=True)
class SchedulingInfo:
    "Provides scheduling information."

    rtprio: tuple[int, int] = resource.getrlimit(  # type: ignore[attr-defined]
        resource.RLIMIT_RTPRIO)  # type: ignore[attr-defined]
    memlock: tuple[int, int] = resource.getrlimit(  # type: ignore[attr-defined]
        resource.RLIMIT_MEMLOCK)  # type: ignore[attr-defined]
    nice: tuple[int, int] = resource.getrlimit(  # type: ignore[attr-defined]
        resource.RLIMIT_NICE)  # type: ignore[attr-defined]

    def __str__(self):
        return (
            f"rtprio: [{self.rtprio[0]}/{self.rtprio[1]}]; "
            f"memlock: [{self.memlock[0]}/{self.memlock[1]}]; "
            f"nice: [{self.nice[0]}/{self.nice[1]}]"
        )

    def __repr__(self):
        return self.__str__()
