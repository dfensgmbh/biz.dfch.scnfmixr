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

"""Module initializing_audio."""

from ...app import ApplicationContext
from ...mixer import AudioMixer
from ..fsm import UiEventInfo
from ..fsm import TransitionBase
from ..fsm import StateBase
from ..fsm import ExecutionContext
from ..transition_event import TransitionEvent


# pylint: disable=R0903
class InitializingAudio(TransitionBase):
    """Initializing the audio system."""

    _app_ctx: ApplicationContext

    def __init__(self, event: str, target: StateBase):

        assert event and event.strip()
        assert target

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.INITIALISING_AUDIO_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.INITIALISING_AUDIO_LEAVE, False),
            target_state=target)

        self._app_ctx = ApplicationContext.Factory.get()

    def invoke(self, ctx: ExecutionContext) -> bool:

        _ = ctx

        mixer = AudioMixer.Factory.get()
        assert mixer is not None

        return True
