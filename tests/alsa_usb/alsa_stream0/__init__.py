# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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

from .epos_expand_30t import INFO as EposExpand30T
from .jabra_evolve_20 import INFO as JabraEvolve20
from .macro_silicon_ms2109 import INFO as MacroSiliconMS2109
from .ugreen_ktmicro import INFO as UgreenKtMicro
from .sound_devices_mixpre6ii import INFO as MixPre6II
from .interface_44100_capture_only import INFO as Capture44100

__all__ = [
    "EposExpand30T",
    "JabraEvolve20",
    "MacroSiliconMS2109",
    "UgreenKtMicro",
    "MixPre6II",
    "Capture44100",
]
