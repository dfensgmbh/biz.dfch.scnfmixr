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

"""Module processing_digit."""

from biz.dfch.logging import log

from ...app import ApplicationContext

from ...ui import StateBase, TransitionBase
from ...ui import UiEventInfo

from ..states import SetDate, SetTime, SetName
from ..transition_event import TransitionEvent


class ProcessingDigit(TransitionBase):
    """Processes a single digit."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT_ENTER, False),
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT_LEAVE, False),
            target_state=target)

    def invoke(self, ctx):

        log.info("ctx.source: '%s'. ctx.event: '%s'.", ctx.source, ctx.event)

        app_ctx = ApplicationContext.Factory.get()

        if SetDate.__name__ == ctx.source:
            log.debug("Processing date ...")
            return app_ctx.date_time_name_input.add_to_date(ctx.event)

        if SetTime.__name__ == ctx.source:
            log.debug("Processing time ...")
            return app_ctx.date_time_name_input.add_to_time(ctx.event)

        if SetName.__name__ == ctx.source:
            log.debug("Processing name ...")
            return app_ctx.date_time_name_input.add_to_name(ctx.event)

        message = f"Invalid source: '{ctx.source}'."
        log.error(message)
        raise ValueError(message)
