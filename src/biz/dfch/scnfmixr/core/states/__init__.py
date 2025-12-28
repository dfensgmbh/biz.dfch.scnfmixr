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

"""Module states."""

from __future__ import annotations

from .system import System
from .initialise_lcl import InitialiseLcl
from .initialise_hi1 import InitialiseHi1
from .initialise_hi2 import InitialiseHi2
from .initialise_hi3 import InitialiseHi3
from .select_language import SelectLanguage
from .initialise_ex1 import InitialiseEx1
from .initialise_ex2 import InitialiseEx2
from .initialise_rc1 import InitialiseRc1
from .initialise_rc2 import InitialiseRc2

from .set_date import SetDate
from .set_time import SetTime
from .set_name import SetName

from .initialise_audio import InitialiseAudio

from .main import Main
from .onrecord import OnRecord

from .playback import Playback, PlaybackPaused
from .storage_management import StorageManagement

from .final_state import FinalState


__all__ = [
    "System",

    "InitialiseLcl",

    "InitialiseHi1",
    # Currently not used.
    "InitialiseHi2",
    # Currently not used.
    "InitialiseHi3",

    "SelectLanguage",

    "InitialiseEx1",
    "InitialiseEx2",

    "InitialiseRc1",
    "InitialiseRc2",

    "SetDate",
    "SetTime",
    "SetName",

    "InitialiseAudio",

    "Main",
    "OnRecord",

    "Playback",
    "PlaybackPaused",

    "StorageManagement",

    "FinalState",
]
