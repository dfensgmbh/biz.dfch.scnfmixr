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

"""Modules transitions."""

from .returning_true import ReturningTrue
from .returning_false import ReturningFalse

from .selecting_english import SelectingEnglish
from .selecting_german import SelectingGerman
from .selecting_french import SelectingFrench
from .selecting_italian import SelectingItalian

from .detecting_lcl import DetectingLcl
from .skipping_lcl import SkippingLcl

from .detecting_ex1 import DetectingEx1
from .skipping_ex1 import SkippingEx1

from .detecting_ex2 import DetectingEx2
from .skipping_ex2 import SkippingEx2

from .detecting_hi1 import DetectingHi1
from .skipping_hi1 import SkippingHi1
from .detecting_hi2 import DetectingHi2
from .skipping_hi2 import SkippingHi2
from .detecting_hi3 import DetectingHi3
from .skipping_hi3 import SkippingHi3

from .detecting_rc1 import DetectingRc1
from .skipping_rc1 import SkippingRc1
from .cleaning_rc1 import CleaningRc1
from .mounting_rc1 import MountingRc1
from .unmounting_rc1 import UnmountingRc1
from .detecting_rc2 import DetectingRc2
from .skipping_rc2 import SkippingRc2
from .cleaning_rc2 import CleaningRc2
from .mounting_rc2 import MountingRc2
from .unmounting_rc2 import UnmountingRc2

from .processing_digit import (
    ProcessingDigit,
    ProcessingDigit0,
    ProcessingDigit1,
    ProcessingDigit2,
    ProcessingDigit3,
    ProcessingDigit4,
    ProcessingDigit5,
    ProcessingDigit6,
    ProcessingDigit7,
    ProcessingDigit8,
    ProcessingDigit9,
    ProcessingDigitOk,
    ProcessingDigitBackspace,
)

from .initialising_audio import InitialisingAudio
from .starting_recording_mixes import (
    StartingRecordingMx0,
    StartingRecordingMx1,
    StartingRecordingMx2,
)
from .stopping_recording import StoppingRecording
from .stopping_system import StoppingSystem
from .mounting_storage import MountingStorage
from .disconnecting_storage import DisconnectingStorage
from .formatting_storage import (
    FormattingStorage,
    FormattingStorageRc1,
    FormattingStorageRc2,
)

from .setting_cuepoint import SettingCuePoint
from .toggling_mute import TogglingMute
from .showing_status import ShowingStatus

from .selecting_pause import SelectingPause
from .leaving_playback import LeavingPlayback
from .jumping_clip_start import JumpingClipStart
from .jumping_clip_end import JumpingClipEnd
from .jumping_clip_previous import JumpingClipPrevious
from .jumping_clip_next import JumpingClipNext
from .jumping_cue_previous import JumpingCuePrevious
from .jumping_cue_next import JumpingCueNext
from .seeking_previous import SeekingPrevious
from .seeking_next import SeekingNext
from .helping_playback import HelpingPlayback


__all__ = [
    "ReturningTrue",
    "ReturningFalse",

    "SelectingEnglish",
    "SelectingGerman",
    "SelectingFrench",
    "SelectingItalian",

    "DetectingLcl",
    "SkippingLcl",
    "DetectingEx1",
    "SkippingEx1",
    "DetectingEx2",
    "SkippingEx2",

    "DetectingHi1",
    "SkippingHi1",
    "DetectingHi2",
    "SkippingHi2",
    "DetectingHi3",
    "SkippingHi3",

    "DetectingRc1",
    "SkippingRc1",
    "CleaningRc1",
    "MountingRc1",
    "UnmountingRc1",
    "DetectingRc2",
    "SkippingRc2",
    "CleaningRc2",
    "MountingRc2",
    "UnmountingRc2",

    "InitialisingAudio",

    "starting_recording_mixes",
    "SettingDate",
    "MountingStorage",
    "DisconnectingStorage",
    "FormattingStorage",
    "FormattingStorageRc1",
    "FormattingStorageRc2",
    "StoppingSystem",

    "StartingRecordingMx0",
    "StartingRecordingMx1",
    "StartingRecordingMx2",
    "StoppingRecording",
    "TogglingMute",
    "SettingCuePoint",
    "ShowingStatus",

    "ProcessingDigit",
    "ProcessingDigit0",
    "ProcessingDigit1",
    "ProcessingDigit2",
    "ProcessingDigit3",
    "ProcessingDigit4",
    "ProcessingDigit5",
    "ProcessingDigit6",
    "ProcessingDigit7",
    "ProcessingDigit8",
    "ProcessingDigit9",
    "ProcessingDigitOk",
    "ProcessingDigitBackspace",

    "SelectingPause",
    "LeavingPlayback",
    "JumpingClipStart",
    "JumpingClipEnd",
    "JumpingClipPrevious",
    "JumpingClipNext",
    "JumpingCuePrevious",
    "JumpingCueNext",
    "SeekingPrevious",
    "SeekingNext",
    "HelpingPlayback",
]
