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

"""Module user_interaction_audio."""

from biz.dfch.i18n import I18n

from ..application_context import ApplicationContext
from ..public.system.messages import SystemMessage
from ..public.audio import FileFormat
from ..core.fsm import UserInteractionBase
from ..playback.audio_menu import AudioMenu


__all__ = [
    "UserInteractionAudio",
]


class UserInteractionAudio(UserInteractionBase):
    """Audio UI output handling.

    This class will subscribe to messages of type `UiEventInfoMessageBase` and
    publish `UiEventInfoAudioMessage` with the original type and translated
    physical paths (honouring the current language setting).
    """

    _AUDIO_FILE_EXTENSION = f".{FileFormat.WAV.value}"

    _player: AudioMenu
    _i18n: I18n
    _app_ctx: ApplicationContext

    def __init__(self, jack_name: str):

        super().__init__()

        assert jack_name and jack_name.strip()

        self._player = AudioMenu.Factory.get()
        self._player.acquire()

        self._i18n = I18n.Factory.get()

        self._app_ctx = ApplicationContext.Factory.get()

        self._message_queue.register(
            self._on_message,
            lambda e: isinstance(e, SystemMessage.UiEventInfoMessageBase))

    def _on_message(self, message):

        assert isinstance(message, SystemMessage.UiEventInfoMessageBase)

        # DFTODO - adjust to something dynamic.
        # And check if file actually exists with "os.path.isfile".
        path = self._i18n.get_resource_path(
            (f"{message.value.name}"
             f"{self._AUDIO_FILE_EXTENSION}"),
            self._app_ctx.ui_parameters.language)

        self._message_queue.publish(
            SystemMessage.UiEventInfoAudioMessage(
                _type=type(message),
                path=path,
                message=message.value))
