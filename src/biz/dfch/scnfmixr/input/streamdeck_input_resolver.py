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

"""StreamdeckInputResolver class."""

from __future__ import annotations

from pathlib import Path

from ...i18n.i18n import I18n
from ...i18n.language_code import LanguageCode

from ..public.input.input_event_map import InputEventMap
from ..public.input.streamdeck_input import StreamdeckInput
from ..public.input.streamdeck_event_map import StreamdeckEventMap


class StreamdeckInputResolver:
    """
    Resolves a given Streamdeck key that is related to a state to an InputEvent.
    """

    _RES_IMG_DIR: str = "img"

    def resolve(
        self,
        state: str,
        key: StreamdeckInput
    ) -> InputEventMap | None:
        """Resolves a given key to an InputEventMap.

        Args:
            state (str):
                The state name to look up in StreamdeckEventMap.
            key(StreamdeckInput):
                The name of the input key.

        Returns:
            result(InputEventMap | None):
            The InputEventMap associated with the given state and key, or None
            if the state does not exist, the key is not a valid
            StreamdeckInput, or the input is not mapped in that state.
        """

        assert isinstance(state, str) and "" != state.strip()
        assert isinstance(key, StreamdeckInput)

        result: InputEventMap | None = None

        # Examine if name is a specified state in StreamdeckEventMap.
        if state not in StreamdeckEventMap:
            return result

        sd_input_event_map = StreamdeckEventMap[state]

        # Examine if input_ is a specified input for this state.
        if key not in sd_input_event_map:
            return result

        result = sd_input_event_map[key]

        return result

    def get_text(
            self,
            input_event: InputEventMap,
            code: LanguageCode = LanguageCode.DEFAULT
    ) -> str:
        """
        Translates the text of the specified `event` into text for display on
        the Streamdeck.

        :param event: The event to translate.
        :type event: InputEventMap
        :return: The translated text.
        :rtype: str
        """

        assert isinstance(input_event, InputEventMap)
        assert isinstance(code, LanguageCode)

        if LanguageCode.DEFAULT == code:
            code = LanguageCode.EN

        result: str = ""

        match input_event.value:
            case InputEventMap.KEY_ENTER:
                result = "ENTER"
            case InputEventMap.KEY_BACKSPACE:
                result = "DELETE"
            case InputEventMap.KEY_TAB:
                result = "TAB"
            case _:
                result = input_event.value

        return result

    def get_input_event_image(
        self,
        name: str,
        key: StreamdeckInput,
        code: LanguageCode = LanguageCode.DEFAULT
    ) -> str:
        """
        Returns a Path object with the image for the key.

        :param name: The name of the state machine state.
        :type name: str
        :param key: The name of the input key.
        :type key: StreamdeckInput
        :param code: The language code.
        :type code: LanguageCode
        :return: The Path to the image.
        :rtype: Path
        """

        assert isinstance(name, str)
        assert isinstance(key, StreamdeckInput)
        assert isinstance(code, LanguageCode)

        i18n = I18n.Factory.get()

        result: Path = Path("")

        # Get the resource path for image files.
        res_name = i18n.get_default_res_dirname()
        image_path = Path(res_name, type(self)._RES_IMG_DIR)

        # Examine if name is a specified state in StreamdeckEventMap.
        if name not in StreamdeckEventMap:
            image_name = "default.png"
            image_partial = i18n.get_resource_path(
                image_name, code, str(image_path))
            result = Path(image_partial)

            return result

        # Get specified keys for this state.
        state = StreamdeckEventMap[name]

        # Examine if key is a specified input for this state.
        if key not in state:
            image_name = f"{name}-default.png"
            image_partial = i18n.get_resource_path(
                image_name, code, str(image_path))
            result = Path(image_partial)

            return result

        # Get the start of the image file name.
        image_name = f"{name}-{key.name}"

        # Get the partial image file path and name.
        image_partial = i18n.get_resource_path(
            image_name, code, str(image_path))
        result = Path(image_partial)

        parent = result.parent
        wildcard = f"{result.name}*"

        matches = list(parent.glob(wildcard))
        if 0 == len(matches):
            image_name = f"{name}-default.png"
            image_partial = i18n.get_resource_path(
                image_name, code, str(image_path))
            result = Path(image_partial)

            return result

        if 1 == len(matches):
            result = matches[0]

        return result
