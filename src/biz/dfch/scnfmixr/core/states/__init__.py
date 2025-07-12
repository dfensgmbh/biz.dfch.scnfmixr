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

"""Module states."""

from __future__ import annotations

from .final_state import FinalState
from .system_menu import SystemMenu
from .initialise_lcl import InitialiseLcl
from .initialise_hi1 import InitialiseHi1
from .select_language import SelectLanguage
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

from .record import Record
from .onrecord import OnRecord

from .final_state import FinalState


__all__ = [
    "SystemMenu",

    "InitialiseLcl",
    "InitialiseHi1",
    # Currently not used.
    "InitialiseHi2",
    "InitialiseHi3",
    "SelectLanguage",

    "InitialiseEx1",
    "InitialiseEx2",

    "InitialiseRc1",
    "InitialiseRc2",

    "SetDate",
    "SetTime",
    "SetName",

    "FinalState",

    "Record",
    "OnRecord",

    "FinalState",
]
