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
from .audio_player import AudioPlayer
from ..core.fsm import UserInteractionBase
from ..core.fsm import UiEventInfo

__all__ = [
    "UserInteractionAudio",
]


class UserInteractionAudio(UserInteractionBase):
    """Audio UI output handling."""

    def __init__(self, jack_name: str):

        assert jack_name and jack_name.strip()

        self._player = AudioPlayer(jack_name)

    def update(self, item):

        assert item
        assert isinstance(item, UiEventInfo)

        app_ctx = ApplicationContext.Factory.get()

        path = I18n.get_resource_path(f"{item.name}.wav",
                                      app_ctx.ui_parameters.language)

        self._player.clear(True)
        self._player.enqueue((path, item.is_loop))
