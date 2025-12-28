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

"""Module system."""

from __future__ import annotations

from ..message_medium import NotificationMedium
from ...ui import UiEventInfo


class SystemMessage:
    """System messages."""

    class Shutdown(NotificationMedium):
        """System shutdown message.

        Attributes:
            None: This message does not have any parameters.
        """

    class StateMachine:
        """StateMachine status messages."""

        class StateMachineMessageBase(NotificationMedium):
            """StateMachine base message.

            Attributes:
                value (str): The event (state or transition).
            """

            value: str

            def __init__(self, value: str):
                super().__init__()

                self.value = value

        class StateMachineStarting(StateMachineMessageBase):
            """StateMachine is starting.

            Attributes:
                None: This message does not have any parameters.
            """

            def __init__(self):
                super().__init__("")

        class StateMachineStarted(StateMachineMessageBase):
            """StateMachine is starting.

            Attributes:
                None: This message does not have any parameters.
            """

            def __init__(self):
                super().__init__("")

        class StateMachineStopping(StateMachineMessageBase):
            """StateMachine is stopping.

            Attributes:
                None: This message does not have any parameters.
            """

            def __init__(self):
                super().__init__("")

        class StateMachineStopped(StateMachineMessageBase):
            """StateMachine is stopped.

            Attributes:
                None: This message does not have any parameters.
            """

            def __init__(self):
                super().__init__("")

        class StateMachineError(StateMachineMessageBase):
            """StateMachine is in an error state.

            Attributes:
                None: This message does not have any parameters.
            """

            def __init__(self):
                super().__init__("")

        class StateMachineStateEnter(StateMachineMessageBase):
            """StateMachine enters a state.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStateLeave(StateMachineMessageBase):
            """StateMachine leaves a state.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineTransitionEnter(StateMachineMessageBase):
            """StateMachine enters a transition.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineTransitionLeave(StateMachineMessageBase):
            """StateMachine leaves a transition.

            Attributes:
                None: This message does not have any parameters.
            """

    class InputEvent(NotificationMedium):
        """Translated input event.

        Attributes:
            value (str): The translated input event.
        """

        value: str

        def __init__(self, value: str):
            super().__init__()

            self.value = value

    class InputEventFirst(InputEvent):
        """Translated input event at the top of the queue.

        Attributes:
            value (str): The translated input event.
        """

    class InputEventClear(InputEvent):
        """Translated input event that also clears the queue.

        Attributes:
            value (str): The translated input event.
        """

    class UiEventInfoMessageBase(NotificationMedium):
        """UiEventInfo"""

        value: UiEventInfo

        def __init__(self, value: UiEventInfo):
            super().__init__()

            assert isinstance(value, UiEventInfo)

            self.value = value

    class UiEventInfoStateMessage(UiEventInfoMessageBase):
        """UiEventInfoStateMessage"""

    class UiEventInfoStateEnterMessage(UiEventInfoStateMessage):
        """UiEventInfoStateMessage"""

    class UiEventInfoStateLeaveMessage(UiEventInfoStateMessage):
        """UiEventInfoStateMessage"""

    class UiEventInfoTransitionMessage(UiEventInfoMessageBase):
        """UiEventInfoTransitionMessage"""

    class UiEventInfoTransitionEnterMessage(UiEventInfoTransitionMessage):
        """UiEventInfoTransitionMessage"""

    class UiEventInfoTransitionLeaveMessage(UiEventInfoTransitionMessage):
        """UiEventInfoTransitionMessage"""

    class UiEventInfoAudioMessage(NotificationMedium):
        """UiEventInfoAudioMessage"""

        type: type
        path: str
        value: UiEventInfo

        def __init__(
                self,
                _type: type,
                path: str,
                message: SystemMessage.UiEventInfoMessageBase,
        ):
            super().__init__()

            assert _type
            assert path and isinstance(path, str) and path.strip()
            assert message

            self.type = _type
            self.path = path
            self.value = message
