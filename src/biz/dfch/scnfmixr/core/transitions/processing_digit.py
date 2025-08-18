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

from ..states import SetDate, SetTime, SetName

from ..fsm import StateBase, TransitionBase, ExecutionContext, UiEventInfo
from ..transition_event import TransitionEvent


__all__ = [
    "ProcessingDigit",
    "ProcessingDigit0",
    "ProcessingDigit1",
    "ProcessingDigit2",
    "ProcessingDigit3",
    "ProcessingDigit4",
    "ProcessingDigit5",
    "ProcessingDigit6",
    "ProcessingDigit7",
    "ProcessingDigit8",
    "ProcessingDigit9",
    "ProcessingDigitOk",
    "ProcessingDigitBackspace",
]


class ProcessingDigit(TransitionBase):
    """Processes a single digit."""

    def __init__(
        self,
        event: str,
        info_enter: UiEventInfo,
        info_leave: UiEventInfo,
        target_state: StateBase
    ) -> None:

        super().__init__(
            event,
            info_enter=info_enter,
            info_leave=info_leave,
            target_state=target_state)

    def invoke(self, ctx):

        assert isinstance(ctx, ExecutionContext)

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


class ProcessingDigit0(ProcessingDigit):
    """Processes digit 0."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT0_LEAVE, False),
            target_state=target)


class ProcessingDigit1(ProcessingDigit):
    """Processes digit 1."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT1_LEAVE, False),
            target_state=target)


class ProcessingDigit2(ProcessingDigit):
    """Processes digit 2."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT2_LEAVE, False),
            target_state=target)


class ProcessingDigit3(ProcessingDigit):
    """Processes digit 3."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT3_LEAVE, False),
            target_state=target)


class ProcessingDigit4(ProcessingDigit):
    """Processes digit 4."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT4_LEAVE, False),
            target_state=target)


class ProcessingDigit5(ProcessingDigit):
    """Processes digit 5."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT5_LEAVE, False),
            target_state=target)


class ProcessingDigit6(ProcessingDigit):
    """Processes digit 6."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT6_LEAVE, False),
            target_state=target)


class ProcessingDigit7(ProcessingDigit):
    """Processes digit 7."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT7_LEAVE, False),
            target_state=target)


class ProcessingDigit8(ProcessingDigit):
    """Processes digit 8."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT8_LEAVE, False),
            target_state=target)


class ProcessingDigit9(ProcessingDigit):
    """Processes digit 9."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT9_LEAVE, False),
            target_state=target)


class ProcessingDigitOk(ProcessingDigit):
    """Processes ENTER key."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT_OK_LEAVE, False),
            target_state=target)


class ProcessingDigitBackspace(ProcessingDigit):
    """Processes BACKSPACE key."""

    def __init__(self, event: str, target: StateBase):

        super().__init__(
            event,
            info_enter=None,
            info_leave=UiEventInfo(
                TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE, False),
            target_state=target)
