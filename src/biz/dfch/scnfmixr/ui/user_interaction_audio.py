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

    _AUDIO_FILE_EXTENSION = f".{FileFormat.WAV}"

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
