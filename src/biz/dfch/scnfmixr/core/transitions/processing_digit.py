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
