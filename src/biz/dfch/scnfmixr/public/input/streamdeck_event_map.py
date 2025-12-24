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

"""StreamdeckEventMap definition."""

from ...public.input.streamdeck_input import StreamdeckInput

from .input_event_map import InputEventMap

__all__ = [
    "StreamdeckEventMap",
]


# This is the default key map.
_streamdeck_event_map_default: dict[StreamdeckInput, InputEventMap] = {
    StreamdeckInput.KEY_00: InputEventMap.KEY_0,
    StreamdeckInput.KEY_01: InputEventMap.KEY_1,
    StreamdeckInput.KEY_02: InputEventMap.KEY_2,
    StreamdeckInput.KEY_03: InputEventMap.KEY_3,
    StreamdeckInput.KEY_04: InputEventMap.KEY_4,
    StreamdeckInput.KEY_05: InputEventMap.KEY_5,
    StreamdeckInput.KEY_06: InputEventMap.KEY_6,
    StreamdeckInput.KEY_07: InputEventMap.KEY_7,
    StreamdeckInput.KEY_08: InputEventMap.KEY_8,
    StreamdeckInput.KEY_09: InputEventMap.KEY_9,
    StreamdeckInput.KEY_0A: InputEventMap.KEY_ASTERISK,
    StreamdeckInput.KEY_0B: InputEventMap.KEY_HASH,
    StreamdeckInput.KEY_0C: InputEventMap.KEY_ENTER,
    StreamdeckInput.KEY_0D: InputEventMap.KEY_BACKSPACE,
    StreamdeckInput.KEY_0E: InputEventMap.KEY_TAB,
}

StreamdeckEventMap: dict[str, dict[StreamdeckInput, InputEventMap]] = {

    "InitialiseLcl": _streamdeck_event_map_default,
    "InitialiseHi1": _streamdeck_event_map_default,
    "InitialiseHi2": _streamdeck_event_map_default,
    "InitialiseHi3": _streamdeck_event_map_default,
    "InitialiseEx1": _streamdeck_event_map_default,
    "InitialiseEx2": _streamdeck_event_map_default,
    "SelectLanguage": _streamdeck_event_map_default,
    "InitialiseRc1": _streamdeck_event_map_default,
    "InitialiseRc2": _streamdeck_event_map_default,
    "SetDate": _streamdeck_event_map_default,
    "SetTime": _streamdeck_event_map_default,
    "SetName": _streamdeck_event_map_default,
    "Main": {
        StreamdeckInput.KEY_00: InputEventMap.KEY_0,
        StreamdeckInput.KEY_01: InputEventMap.KEY_1,
        StreamdeckInput.KEY_02: InputEventMap.KEY_2,
        StreamdeckInput.KEY_03: InputEventMap.KEY_3,
        StreamdeckInput.KEY_04: InputEventMap.KEY_4,
        StreamdeckInput.KEY_05: InputEventMap.KEY_5,
        StreamdeckInput.KEY_06: InputEventMap.KEY_6,
        StreamdeckInput.KEY_07: InputEventMap.KEY_7,
        StreamdeckInput.KEY_08: InputEventMap.KEY_8,
        StreamdeckInput.KEY_09: InputEventMap.KEY_9,
        StreamdeckInput.KEY_0A: InputEventMap.KEY_ASTERISK,
        StreamdeckInput.KEY_0B: InputEventMap.KEY_HASH,
        StreamdeckInput.KEY_0C: InputEventMap.KEY_ENTER,
        StreamdeckInput.KEY_0D: InputEventMap.KEY_BACKSPACE,
        StreamdeckInput.KEY_0E: InputEventMap.KEY_TAB,
    },
    "OnRecord": _streamdeck_event_map_default,
    "InitialiseAudio": _streamdeck_event_map_default,
    "Playback": _streamdeck_event_map_default,
    "PlaybackPaused": _streamdeck_event_map_default,
    "System": _streamdeck_event_map_default,
    "StorageManagement": _streamdeck_event_map_default,
    "FinalState": _streamdeck_event_map_default,
}
