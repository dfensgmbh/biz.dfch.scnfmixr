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

"""534d:2109 MacroSilicon USB Video

Atomos Connect 4K

Note: Atomos has a 'continuous' interface rate.
"""

INFO = """\
MacroSilicon MS2109 at usb-xhci-hcd.0-1.2, high speed : USB Audio

Capture:
  Status: Stop
  Interface 3
    Altset 1
    Format: S16_LE
    Channels: 2
    Endpoint: 0x82 (2 IN) (ASYNC)
    Rates: 48000 - 48000 (continuous)
    Data packet interval: 1000 us
    Bits: 0
""".splitlines()  # noqa: E501 # pylint: disable=C0301
