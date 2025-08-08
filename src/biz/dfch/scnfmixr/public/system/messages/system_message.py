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

        class StateMachineStarting(NotificationMedium):
            """StateMachine is starting.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStarted(NotificationMedium):
            """StateMachine is starting.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStopping(NotificationMedium):
            """StateMachine is stopping.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStopped(NotificationMedium):
            """StateMachine is stopped.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineError(NotificationMedium):
            """StateMachine is in an error state.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStateEnter(NotificationMedium):
            """StateMachine enters a state.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineStateLeave(NotificationMedium):
            """StateMachine leaves a state.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineTransitionEnter(NotificationMedium):
            """StateMachine enters a transitition.

            Attributes:
                None: This message does not have any parameters.
            """

        class StateMachineTransitionLeave(NotificationMedium):
            """StateMachine leaves a transitition.

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
