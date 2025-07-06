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

"""Module SelectingItalian."""

from biz.dfch.logging import log

from ...app import ApplicationContext
from ...ui import LanguageCode
from ...ui import UiEventInfo
from ...ui import ExecutionContext
from ...ui import TransitionBase
from ...ui import StateBase
from ..transition_event import TransitionEvent


class SelectingItalian(TransitionBase):
    """Class SelectingItalian."""

    def __init__(self, event: str, target: StateBase):
        """Default ctor."""

        super().__init__(
            event=event,
            info_enter=UiEventInfo(
                TransitionEvent.SELECTING_ITALIAN_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.SELECTING_ITALIAN_LEAVE, False),
            target_state=target)

    def invoke(self, ctx: ExecutionContext) -> bool:

        assert ctx and isinstance(ctx, ExecutionContext)

        previous = ApplicationContext().language
        ApplicationContext().language = LanguageCode.IT

        log.info("Set language from '%s' to '%s'.",
                 previous, ApplicationContext().language)

        return True
