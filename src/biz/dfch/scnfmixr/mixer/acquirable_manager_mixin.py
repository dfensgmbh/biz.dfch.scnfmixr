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

"""Module acquirable_manager_mixin."""

from abc import ABC, abstractmethod
from typing import Self

from biz.dfch.logging import log
from biz.dfch.scnfmixr.public.messages import (
    MessageBase,
    SystemMessage,
    Topology
)
from biz.dfch.scnfmixr.public.mixer import IAcquirable
from biz.dfch.scnfmixr.system import MessageQueue


class AcquirableManagerMixin(IAcquirable, ABC):
    """AcquirableManagerMixin"""

    _is_acquired: bool
    _mq: MessageQueue

    def __init__(self):
        super().__init__()

        self._mq = MessageQueue.Factory.get()

    def acquire(self) -> Self:

        if self._is_acquired:
            return self

        try:
            log.debug("Signal manager starting ...")

            self._mq.register(
                self._on_message,
                lambda e: isinstance(
                    e,
                    # (SystemMessage.Shutdown, Topology.ChangedNotification)))
                    (SystemMessage.Shutdown)))

            self._mq.publish(
                Topology.SignalManagerStartingNotification(str(type(self))))

            result = self.do_acquire()

            self._mq.publish(
                Topology.SignalManagerStartedNotification(str(type(self))))

            self._is_acquired = True

            log.info("Signal manager starting OK.")

            return result

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(
                Topology.SignalManagerErrorNotification(str(type(self))))
            log.error("Signal manager starting FAILED. [%s]", ex, exc_info=True)

    def release(self) -> None:

        if not self._is_acquired:
            return

        try:
            log.debug("Signal manager stopping ...")

            self._mq.publish(
                Topology.SignalManagerStoppingNotification(str(type(self))))

            self.do_release()

            self._mq.unregister(self._on_message)

            self._mq.publish(
                Topology.SignalManagerStoppedNotification(str(type(self))))

            log.info("Signal manager stopping OK.")

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(
                Topology.SignalManagerErrorNotification(str(type(self))))
            log.error("Signal manager stopping FAILED. [%s]", ex, exc_info=True)

    @abstractmethod
    def do_acquire(self) -> Self:
        """Actual acquisition implementation."""

        raise NotImplementedError

    @abstractmethod
    def do_release(self):
        """Actual release implementation."""

        raise NotImplementedError

    @abstractmethod
    def _on_message(self, message: MessageBase):
        """Message handler."""

        raise NotImplementedError
