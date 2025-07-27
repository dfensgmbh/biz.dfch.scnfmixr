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
