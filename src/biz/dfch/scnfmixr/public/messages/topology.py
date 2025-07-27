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

"""Module Module."""

from __future__ import annotations

from ..system import (
    NotificationMedium,
)
from ...public.mixer import ConnectionInfo

__all__ = [
    "Topology",
]


class Topology:
    """Topology related messages."""

    class ChangedNotification(NotificationMedium):
        """Notifies about a change in topology."""

        value: ConnectionInfo

        def __init__(self, value: ConnectionInfo):
            super().__init__()

            assert isinstance(value, ConnectionInfo)

            self.value = ConnectionInfo(value.clone())

    class TopologyValueNotificationBase(NotificationMedium):
        """Base notification with a value property."""

        value: str

        def __init__(self, value: str):
            super().__init__()

            assert isinstance(value, str) and value.strip()

            self.value = value

    class DeviceErrorNotification(TopologyValueNotificationBase):
        """Notification when an device error occurred."""

    class DeviceAddingNotification(TopologyValueNotificationBase):
        """Notification when a new device is being added."""

    class DeviceAddedNotification(TopologyValueNotificationBase):
        """Notification when a new device is added."""

    class DeviceRemovingNotification(TopologyValueNotificationBase):
        """Notification when an existing device is being removed."""

    class DeviceRemovedNotification(TopologyValueNotificationBase):
        """Notification when an existing device is removed."""

    class PointErrorNotification(TopologyValueNotificationBase):
        """Notification when an point error occurred."""

    class PointAddingNotification(TopologyValueNotificationBase):
        """Notification when a new point is being added."""

    class PointAddedNotification(TopologyValueNotificationBase):
        """Notification when a new point is added."""

    class PointLostNotification(TopologyValueNotificationBase):
        """Notification when a point was lost."""

    class PointFoundNotification(TopologyValueNotificationBase):
        """Notification when a point was found."""

    class PointRemovingNotification(TopologyValueNotificationBase):
        """Notification when an existing point is being removed."""

    class PointRemovedNotification(TopologyValueNotificationBase):
        """Notification when an existing point is removed."""

    # Point: new lifecycle definitions.
    # Defining - > Defined - > Activated ->
    # possibly: Lost/Found
    # Deactivated - > Undefining - > Undefined
    class PointActivatedNotification(TopologyValueNotificationBase):
        """Notification when a new point has been activated."""

    class PointDeactivatedNotification(TopologyValueNotificationBase):
        """Notification when an existing point has been deactivated."""

    class PointZombieNotification(TopologyValueNotificationBase):
        """Notification when a removed point is stil found."""

    # Path: lifecycle definitions.
    class PathErrorNotification(TopologyValueNotificationBase):
        """Notification when a new path is being added."""

    class PathDefiningNotification(TopologyValueNotificationBase):
        """Notification when a new path is being defined."""

    class PathDefinedNotification(TopologyValueNotificationBase):
        """Notification when a new path is defined."""

    class PathConnectingNotification(TopologyValueNotificationBase):
        """Notification when a new path is waiting to be connected."""

    class PathConnectedNotification(TopologyValueNotificationBase):
        """Notification when a new path is connected."""

    class PathUndefiningNotification(TopologyValueNotificationBase):
        """Notification when a path is being undefined."""

    class PathUndefinedNotification(TopologyValueNotificationBase):
        """Notification when a path is undefined."""

    class PathDisconnectingNotification(TopologyValueNotificationBase):
        """Notification when an existing path is being disconnected."""

    class PathDisconnectedNotification(TopologyValueNotificationBase):
        """Notification when an existing path is disconnected."""

    class PathLostNotification(TopologyValueNotificationBase):
        """Notification when an existing path is lost."""

    class PathFoundNotification(TopologyValueNotificationBase):
        """Notification when a lost path is found."""

    class PathZombieNotification(TopologyValueNotificationBase):
        """Notification when a removed path is stil found."""

    class SignalManagerErrorNotification(TopologyValueNotificationBase):
        """Notification when the point and path manager is in an error state."""

    class SignalManagerStartingNotification(TopologyValueNotificationBase):
        """Notification when the point and path manager is starting."""

    class SignalManagerStartedNotification(TopologyValueNotificationBase):
        """Notification when the point and path manager is started."""

    class SignalManagerStoppingNotification(TopologyValueNotificationBase):
        """Notification when the point and path manager is stopping."""

    class SignalManagerStoppedNotification(TopologyValueNotificationBase):
        """Notification when the point and path manager is stopped."""
