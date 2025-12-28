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
