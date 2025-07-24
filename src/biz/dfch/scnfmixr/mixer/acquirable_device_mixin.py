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

"""Module acquirable_device_mixin."""

from abc import ABC, abstractmethod
from typing import Self

from biz.dfch.logging import log
from biz.dfch.scnfmixr.public.messages import MessageBase, Topology
from biz.dfch.scnfmixr.public.mixer import IAcquirable
from biz.dfch.scnfmixr.system import MessageQueue


class AcquirableDeviceMixin(IAcquirable, ABC):
    """JackAlsaDeviceAcquirableMixin

    Implements a resource manager with message queue notification.
    """

    _is_acquired: bool
    _mq: MessageQueue

    def __init__(self):
        super().__init__()

        self._mq = MessageQueue.Factory.get()

    def acquire(self) -> Self:
        if self._is_acquired:
            return self

        try:
            log.debug("Acquiring resource ...")

            self._mq.register(
                self._on_message,
                lambda e: isinstance(e, Topology.ChangedNotification))

            self._mq.publish(Topology.DeviceAddingNotification(self.name))

            result = self.do_acquire()

            self._mq.publish(Topology.DeviceAddedNotification(self.name))

            self._is_acquired = True

            log.info("Acquiring resource OK.")

            return result

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(Topology.DeviceErrorNotification(self.name))
            log.error("Acquiring resource FAILED. [%s]", ex, exc_info=True)

    def release(self) -> None:

        if not self._is_acquired:
            return

        try:
            log.debug("Releasing resource ...")

            self.do_release()

            self._mq.unregister(self._on_message)

            log.info("Releasing resource OK.")

        except Exception as ex:  # pylint: disable=W0718

            self._mq.publish(Topology.DeviceErrorNotification(self.name))
            log.error("Releasing resource FAILED. [%s]", ex, exc_info=True)

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
