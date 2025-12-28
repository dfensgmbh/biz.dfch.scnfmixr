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

"""Module starting_recording_mixes."""

from biz.dfch.scnfmixr.public.mixer import MixbusDevice
from .starting_recording import StartingRecording


class StartingRecordingMx0(StartingRecording):
    """Starts a recording for MX0."""

    def __init__(self, event, target):
        super().__init__(event, target, [MixbusDevice.MX0])


class StartingRecordingMx1(StartingRecording):
    """Starts a recording for MX0, MX1"""

    def __init__(self, event, target):
        super().__init__(event, target, [MixbusDevice.MX0, MixbusDevice.MX1])


class StartingRecordingMx2(StartingRecording):
    """Starts a recording for MX0, MX1, MX2."""

    def __init__(self, event, target):
        super().__init__(event, target, [
            MixbusDevice.MX0, MixbusDevice.MX1, MixbusDevice.MX2])
