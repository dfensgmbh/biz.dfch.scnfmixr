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

"""Package input."""

from __future__ import annotations

from .event_map_base import EventMapBase
from .input_device import InputDevice
from .input_event_map import InputEventMap
from .keyboard_event_map import KeyboardEventMap
from .menu_profile import MenuProfile
from .streamdeck_input import StreamdeckInput
from .streamdeck_event_map import StreamdeckEventMap

__all__ = [
    "EventMapBase",
    "InputDevice",
    "KeyboardEventMap",
    "MenuProfile",
    "InputEventMap",
    "StreamdeckInput",
    "StreamdeckEventMap",
]
