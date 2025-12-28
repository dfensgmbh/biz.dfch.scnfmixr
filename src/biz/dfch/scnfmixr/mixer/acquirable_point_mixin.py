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

"""Module acquirable_point_mixin."""

from abc import ABC, abstractmethod
from typing import Self

from biz.dfch.logging import log
from biz.dfch.scnfmixr.public.messages import MessageBase, Topology
from biz.dfch.scnfmixr.public.mixer import IAcquirable
from biz.dfch.scnfmixr.system import MessageQueue


class AcquirablePointMixin(IAcquirable, ABC):
    """AcquirablePointMixin

    Implements a resource manager with message queue notification.
    """

    _resource_name: str
    _mq: MessageQueue

    def __init__(self):
        super().__init__()

        self._mq = MessageQueue.Factory.get()

    def acquire(self) -> Self:
        if self.is_acquired:
            return self

        try:
            name = getattr(self, "name", "<?>")

            log.debug("Acquiring resource point '%s' ...", name)

            # self._mq.register(
            #     self._on_message,
            #     lambda e: isinstance(e, Topology.ChangedNotification))

            self._mq.publish(
                Topology.PointAddingNotification(name))

            result = self.do_acquire()

            self._mq.publish(
                Topology.PointAddedNotification(name))

            self.is_acquired = True

            log.info("Acquiring resource point '%s' OK.", name)

            return result

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(
                Topology.PointErrorNotification(name))
            log.error(
                "Acquiring resource point '%s' FAILED. [%s]",
                name, ex, exc_info=True)

    def release(self) -> None:

        if not self.is_acquired:
            return

        name = getattr(self, "name", "<?>")

        try:
            log.debug("Releasing resource point '%s' ...", name)

            self._mq.publish(
                Topology.PointRemovingNotification(name))

            self.do_release()

            self.is_acquired = False

            self._mq.publish(
                Topology.PointRemovedNotification(name))

            # self._mq.unregister(self._on_message)

            log.info("Releasing resource point '%s' OK.", name)

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(
                Topology.PointErrorNotification(name))
            log.error(
                "Releasing resource point '%s' FAILED. [%s]",
                name, ex, exc_info=True)

    @abstractmethod
    def do_acquire(self) -> Self:
        """Actual acquisition implementation."""

        name = getattr(self, "name", "<?>")
        log.critical(
            "do_acquire: You should NEVER see this message [%s].", name)

        raise NotImplementedError

    @abstractmethod
    def do_release(self):
        """Actual release implementation."""

        name = getattr(self, "name", "<?>")
        log.critical(
            "do_release: You should NEVER see this message [%s].", name)

        raise NotImplementedError

    @abstractmethod
    def _on_message(self, message: MessageBase):
        """Message handler."""

        raise NotImplementedError

    @property
    @abstractmethod
    def is_acquired(self):
        raise NotImplementedError

    @is_acquired.setter
    @abstractmethod
    def is_acquired(self, value):
        raise NotImplementedError
