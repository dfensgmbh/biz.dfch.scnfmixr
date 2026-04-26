# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

from ...app import ApplicationContext

from .starting_recording import StartingRecording


class StartingRecordingMixes(StartingRecording):
    """Starts a recording specified MixBusDevice from `--record-target`."""

    def __init__(self, event, target):
        app_ctx = ApplicationContext.Factory.get()
        targets = app_ctx.recording_parameters.targets

        super().__init__(event, target, targets)
