# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

from .epos_expand_30t import INFO as EposExpand30T
from .epos_expand_40t import INFO as EposExpand40T
from .jabra_evolve_20 import INFO as JabraEvolve20
from .jabra_speak_510_0420 import INFO as JabraSpeak5100420
from .jabra_speak_510_0422 import INFO as JabraSpeak5100422
from .jabra_speak2_J75 import INFO as JabraSpeak2J75
from .macro_silicon_ms2109 import INFO as MacroSiliconMS2109
from .ugreen_ktmicro import INFO as UgreenKtMicro
from .sound_devices_mixpre3ii_2020 import INFO as MixPre3II2020
from .sound_devices_mixpre6ii import INFO as MixPre6II
from .interface_44100_capture_only import INFO as Capture44100
from .icybox_ib_ac527 import INFO as IcyBoxAc527
from .sabrent import INFO as Sabrent
from .ugreen_a2 import INFO as UgreenA2
from .antlion_audio import INFO as Antlion
from .roland_sp404mkii import INFO as RolandSP404MKII

__all__ = [
    "EposExpand30T",
    "EposExpand40T",
    "JabraEvolve20",
    "JabraSpeak5100420",
    "JabraSpeak5100422",
    "JabraSpeak2J75",
    "MacroSiliconMS2109",
    "UgreenKtMicro",
    "MixPre3II2020",
    "MixPre6II",
    "Capture44100",
    "IcyBoxAc527",
    "Sabrent",
    "UgreenA2",
    "Antlion",
    "RolandSP404MKII",
]
