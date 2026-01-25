# Copyright (c) 2026 d-fens GmbH, http://d-fens.ch
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

"""menu_profile"""

from __future__ import annotations

from enum import auto, StrEnum

from .event_map_base import EventMapBase
from .input_device import InputDevice
from .keyboard_event_map import KeyboardEventMap
from .streamdeck_event_map import StreamdeckEventMap


class MenuProfile(StrEnum):
    """
    Defines menu profiles.

    A profile changes the selection of the event maps.

    See: KeyboardEventMap, StreamdeckEventMap.
    """

    # The full functionality and user interface.
    DEFAULT = auto()

    # Only single record command.
    RECORDER = auto()

    # Only playback functionality.
    PLAYBACK = auto()

    def get_event_map(self, input_device: InputDevice) -> type[EventMapBase]:
        """
        This method returns the class type of the input device for the current
        menu profile option.
        """

        assert isinstance(input_device, InputDevice)

        _map: dict[MenuProfile, dict[InputDevice, type[EventMapBase]]] = {
            MenuProfile.DEFAULT: {
                InputDevice.HI1: KeyboardEventMap,
                InputDevice.HI2: StreamdeckEventMap,
            },
            MenuProfile.RECORDER: {
                InputDevice.HI1: KeyboardEventMap,
                InputDevice.HI2: StreamdeckEventMap,
            },
            MenuProfile.PLAYBACK: {
                InputDevice.HI1: KeyboardEventMap,
                InputDevice.HI2: StreamdeckEventMap,
            },
        }

        match input_device:
            case InputDevice.HI1 | InputDevice.HI2:
                _type = _map[self][input_device]
                assert _type is not None
                return _type
            case InputDevice.HI3:
                raise NotImplementedError(
                    f"Invalid input device '{input_device}'.")
            case _:
                raise LookupError(f"Invalid input device '{input_device}'.")
