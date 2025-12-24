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

"""Package input."""

from __future__ import annotations

from ..public.input.input_event_map import InputEventMap
from ..public.input.streamdeck_input import StreamdeckInput
from ..public.input.streamdeck_event_map import StreamdeckEventMap


class StreamdeckInputResolver:
    """
    Resolves a given Streamdeck key that is related to a state to an InputEvent.
    """

    def invoke(self, name: str, key: int) -> InputEventMap | None:
        """Resolves a given key to an InputEventMap.

        Args:
            name (str):
                The state name to look up in StreamdeckEventMap.
            key (int):
                The integer value to convert to a StreamdeckInput enum
                member.

        Returns:
            result(InputEventMap | None):
            The InputEventMap associated with the given state and key, or None
            if the state does not exist, the key is not a valid
            StreamdeckInput, or the input is not mapped in that state.
        """

        assert isinstance(name, str) and "" != name.strip()
        assert isinstance(key, int)

        result: InputEventMap | None = None

        # Examine if name is a specified state in StreamdeckEventMap.
        if name not in StreamdeckEventMap:
            return result

        state = StreamdeckEventMap[name]

        # Examine if key is a specified StreamdeckInput.
        try:
            sd_input: StreamdeckInput = StreamdeckInput(key)
        except ValueError:
            return result

        # Examine if input_ is a specified input for this state.
        if sd_input not in state:
            return result

        result = state[sd_input]

        return result
