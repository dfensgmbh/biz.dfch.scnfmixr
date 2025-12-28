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

"""Module audio_menu."""

from __future__ import annotations
from threading import Event, Lock, Thread
import time
from typing import ClassVar, Callable, Any

from biz.dfch.logging import log
from biz.dfch.asyn import ConcurrentDoubleSideQueueT

from ..system import MessageQueue
from ..public.mixer import IAcquirable
from ..public.storage import MountPoint
from ..public.messages import MessageBase, SystemMessage
from ..public.system.messages import SystemMessage as msgt

from .media_player_type import MediaPlayerType
from .media_player_client import MediaPlayerClient

__all__ = [
    "AudioMenu",
]


class AudioMenu(IAcquirable):
    """The audio menu player.

    How does it work?

    When the menu is running, new audio menu items to play are received via
    `_on_message` (message of type `SystemMessage.UiEventInfoAudioMessage`).
    These messages are then enqueued on an internal queue, a signal is set, and
    the `_worker` thread will be woken up and process the messages.
    Depending on message type (state enter, state leave, transition enter,
    transition leave), a handler will be invoked synchronously.
    """

    _WORKER_SIGNAL_WAIT_TIME_MS = 10000
    _EXCEPTION_TIMEOUT_MS = 1000

    _message_handler: dict[type, Callable[[Any], None]]

    _is_acquired: bool
    _sync_root: Lock
    _signal: Event
    _worker_do_stop: bool
    _mq: MessageQueue
    _worker_thread: Thread
    _queue: ConcurrentDoubleSideQueueT[SystemMessage.UiEventInfoAudioMessage]
    _client: MediaPlayerClient | None
    _queued_items: dict[str, list[int]]
    _current_message: msgt.UiEventInfoAudioMessage | None

    def __init__(self):
        """Private ctor.

        Raises:
            AssertionError: If called directly.
        """

        if not AudioMenu.Factory._sync_root.locked():
            raise AssertionError("Private ctor. Use Factory instead.")

        log.debug("Initializing ...")

        self._is_acquired = False
        self._sync_root = Lock()
        self._signal = Event()
        self._mq = MessageQueue.Factory.get()
        self._worker_do_stop = False
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._queue = ConcurrentDoubleSideQueueT[SystemMessage.UiEventInfoAudioMessage]()  # noqa: E501
        self._client = None
        self._queued_items: dict[str, list[int]] = {}
        self._current_message = None

        self._message_handler: dict[type, Callable[[Any], None]] = {
            msgt.UiEventInfoStateEnterMessage: self._on_state_enter,
            msgt.UiEventInfoStateLeaveMessage: self._on_state_leave,
            msgt.UiEventInfoTransitionEnterMessage: self._on_transition_enter,
            msgt.UiEventInfoTransitionLeaveMessage: self._on_transition_leave,
        }

        log.info("Initializing OK.")

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[AudioMenu] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def get() -> AudioMenu:
            """Creates or gets the instance of the audio playback player."""

            if AudioMenu.Factory.__instance is not None:
                return AudioMenu.Factory.__instance

            with AudioMenu.Factory._sync_root:

                if AudioMenu.Factory.__instance is not None:
                    return AudioMenu.Factory.__instance

                AudioMenu.Factory.__instance = AudioMenu()

            # Note: here we acquire the class directly after creating the
            # singleton, which might not be totally intuitive! On the other
            # it does not make sense to get the singleton and acquire each time
            # after it.
            AudioMenu.Factory.__instance.acquire()

            return AudioMenu.Factory.__instance

    def _worker(self) -> None:
        """Worker thread for processing messages."""

        log.debug("_worker: Initializing ...")

        signal_wait_time_s = self._WORKER_SIGNAL_WAIT_TIME_MS / 1000

        start = time.monotonic()

        log.info("_worker: Initializing OK.")

        log.debug("_worker: Executing ...")

        while not self._worker_do_stop:
            try:
                now = time.monotonic()
                if now > start + signal_wait_time_s:
                    delta = now - start
                    start = now
                    log.debug("_worker: Keep alive [%sms].", int(delta*1000))

                result = self._signal.wait(signal_wait_time_s)
                self._signal.clear()
                if not result:
                    continue

                while True:
                    message = self._queue.dequeue()
                    if message is None:
                        break

                    handler = self._message_handler.get(message.type)
                    if handler is None:
                        log.warning("_worker: Unrecognised message: '%s' [%s].",
                                    type(message).__name__,
                                    message.name)
                        continue

                    log.debug(
                        "_worker: Processing message '%s': '%s' ...",
                        message.type.__name__,
                        message.path)

                    handler(message)
                    self._current_message = message

                    log.info(
                        "_worker: Processing message '%s': '%s' OK.",
                        message.type.__name__,
                        message.path)

            except Exception as ex:  # pylint: disable=W0718
                log.error("_worker: An error occurred: '%s'. Waiting %sms ...",
                          ex,
                          self._EXCEPTION_TIMEOUT_MS,
                          exc_info=True)
                time.sleep(self._EXCEPTION_TIMEOUT_MS / 1000)

        log.info("_worker: Executing OK.")

    def _on_message(self, message: MessageBase):
        """Message handler."""

        if isinstance(message, SystemMessage.Shutdown):
            self.release()
            return

        if isinstance(message, SystemMessage.UiEventInfoAudioMessage):
            log.debug("_on_message: [type: '%s'] [path: '%s']", type(
                message).__name__, message.path)
            self._queue.enqueue(message)
            self._signal.set()
            return

        log.warning("Unrecognised message received: '%s' [%s].",
                    type(message).__name__,
                    message.name)

    def _on_state_enter(
        self,
        message: msgt.UiEventInfoAudioMessage
    ) -> None:
        """UiEventInfoStateEnterMessage"""

        assert isinstance(message, msgt.UiEventInfoAudioMessage)
        assert message.type is msgt.UiEventInfoStateEnterMessage

        log.debug("_on_state_enter ...")
        result = self._client.load_resource_queue(lambda e: e in message.path)
        if 0 >= len(result):
            log.warning("_on_state_enter: no file found.")
            return

        log.info("_on_state_enter [%s].", result)
        self._client.start()

    def get_fullname(self, value: str) -> str:
        """Returns the full path based on value from `MountPoint`."""

        assert isinstance(value, str) and value.strip()

        value_lower = value.lower()
        for mp in MountPoint:
            mp_lower = mp.name.lower()
            if not value_lower.startswith(mp_lower):
                continue

            return f"{mp.value}{value.removeprefix(mp_lower)}"

    def _on_state_leave(
        self,
        message: msgt.UiEventInfoAudioMessage
    ) -> None:
        """UiEventInfoStateLeaveMessage"""

        assert isinstance(message, msgt.UiEventInfoAudioMessage)
        assert message.type is msgt.UiEventInfoStateLeaveMessage

        log.debug("_on_state_leave ...")
        self._client.clear()
        result = self._client.load_resource_queue(lambda e: e in message.path)
        if 0 >= len(result):
            log.warning("_on_state_leave: no file found.")
            return

        log.info("_on_state_leave [%s].", result)
        self._client.start()

    def _on_transition_enter(
        self,
        message: msgt.UiEventInfoAudioMessage
    ) -> None:
        """UiEventInfoTransitionEnterMessage"""

        assert isinstance(message, msgt.UiEventInfoAudioMessage)
        assert message.type is msgt.UiEventInfoTransitionEnterMessage

        log.debug("_on_transition_enter ...")
        result = self._client.load_resource_queue(lambda e: e in message.path)
        if 0 >= len(result):
            log.warning("_on_transition_enter: no file found.")
            return

        log.info("_on_transition_enter [%s].", result)
        self._client.start()

    def _on_transition_leave(
        self,
        message: msgt.UiEventInfoAudioMessage
    ) -> None:
        """UiEventInfoTransitionLeaveMessage"""

        assert isinstance(message, msgt.UiEventInfoAudioMessage)
        assert message.type is msgt.UiEventInfoTransitionLeaveMessage

        log.debug("_on_transition_leave ...")
        self._client.clear()
        result = self._client.load_resource_queue(lambda e: e in message.path)
        if 0 >= len(result):
            log.warning("_on_transition_leave: no file found.")
            return

        log.info("_on_transition_leave [%s].", result)
        self._client.start()

    @property
    def is_acquired(self):
        return self._is_acquired

    @is_acquired.setter
    def is_acquired(self, value):

        assert isinstance(value, bool)

        self._is_acquired = value

    def acquire(self):
        if self._is_acquired:
            return self

        with self._sync_root:
            if self._is_acquired:
                return self

            log.debug("Acquiring resources ...")

            self._client = MediaPlayerClient(MediaPlayerType.MENU)
            self._client.set_consume(True)
            self._client.acquire()

            self._worker_do_stop = False
            self._signal.clear()
            self._worker_thread.start()
            self._mq.register(
                self._on_message,
                lambda e: isinstance(
                    e, (SystemMessage.Shutdown,
                        SystemMessage.UiEventInfoAudioMessage)))

            self._is_acquired = True

        log.info("Acquiring resources OK.")

        return self

    def release(self):
        if not self._is_acquired:
            return

        with self._sync_root:
            if not self._is_acquired:
                return

            log.debug("Releasing resources ...")

            self._mq.unregister(self._on_message)
            self._worker_do_stop = True
            self._worker_thread.join()

            self._client.release()

            self._is_acquired = False

        log.info("Releasing resources OK.")
