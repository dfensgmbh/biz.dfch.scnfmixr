# # MIT License

# # Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:

# # The above copyright notice and this permission notice shall be included in all
# # copies or substantial portions of the Software.

# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# # SOFTWARE.

# """Module jack_signal_point_manager."""

# from __future__ import annotations
# import logging
# import threading
# import time
# from typing import ClassVar


# from biz.dfch.logging import log
# from biz.dfch.scnfmixr.mixer.jack_alsa_device import (
#     JackAlsaSinkPoint,
#     JackAlsaSourcePoint,
# )
# from biz.dfch.scnfmixr.mixer.thread_pool import ThreadPool
# from biz.dfch.scnfmixr.public.messages import Topology
# from biz.dfch.scnfmixr.public.mixer import ConnectionInfo
# from biz.dfch.scnfmixr.public.mixer.iconnectable_point import IConnectablePoint
# from biz.dfch.scnfmixr.public.mixer.state import State


# class JackSignalPointManager:
#     """Manager for JACK signal points."""

#     _WAIT_INTERVAL_S: int = 1
#     _KEEP_ALIVE_INTERVAL_S = 10

#     _thread_pool: ThreadPool

#     _is_acquired: bool
#     _sync_root: threading.Lock
#     _signal: threading.Event
#     _signal_shutdown: threading.Event
#     _points: dict[str, tuple[State, IConnectablePoint]]

#     _worker_signal_stop: threading.Event
#     _worker_thread: threading.Thread

#     def __init__(self):
#         """Private ctor. Use Factory to create an instance of this object."""

#         if not JackSignalPointManager.Factory._sync_root.locked():
#             raise RuntimeError("Private ctor. Use Factory instead.")

#         super().__init__()

#         self._thread_pool = ThreadPool.Factory.get()
#         self._is_acquired = False
#         self._sync_root = threading.Lock()
#         self._signal = threading.Event()
#         self._signal_shutdown = threading.Event()
#         self._points = {}
#         self._worker_signal_stop = threading.Event()
#         self._worker_thread = threading.Thread(target=self._worker, daemon=True)

#     class Factory:  # pylint: disable=R0903
#         """Factory class."""

#         __instance: ClassVar[JackSignalPointManager | None] = None
#         _sync_root: ClassVar[threading.Lock] = threading.Lock()

#         @staticmethod
#         def get() -> JackSignalPointManager:
#             """Gets the singleton."""

#             if JackSignalPointManager.Factory.__instance is not None:
#                 return JackSignalPointManager.Factory.__instance

#             with JackSignalPointManager.Factory._sync_root:

#                 if JackSignalPointManager.Factory.__instance is not None:
#                     return JackSignalPointManager.Factory.__instance

#                 JackSignalPointManager.Factory.__instance = (
#                     JackSignalPointManager()
#                 )

#             return JackSignalPointManager.Factory.__instance

#     class SuppressNoisyDebug(logging.Filter):
#         """Supress DEBUG level logging of module MultiLineTextParser
#         and process."""

#         def filter(self, record) -> bool:

#             if (record.levelno == logging.DEBUG
#                     and record.module in ("MultiLineTextParser")):
#                 return False
#             if (record.levelno in (logging.DEBUG, logging.INFO)
#                     and record.module in ("process")):
#                 return False
#             return True

#     def _worker(self) -> None:
#         """Worker continuously getting JACK topology."""

#         log.debug("_worker: Initializing ...")

#         previous: dict[tuple[str, bool], list[str]] = {}
#         start = time.monotonic()
#         log_filter = JackSignalPointManager.SuppressNoisyDebug()

#         log.info("_worker: Initializing OK.")

#         log.debug("_worker: Processing ...")

#         while not self._worker_signal_stop.wait(self._WAIT_INTERVAL_S):

#             try:
#                 now = time.monotonic()
#                 if now > start + self._KEEP_ALIVE_INTERVAL_S:
#                     start = now
#                     log.debug("_worker: Keep alive.")

#                 # DFTODO: Quirky and not thread safe. Maybe subclass and lock?
#                 log.addFilter(log_filter)
#                 result = JackConnection.get_connections3()
#                 log.removeFilter(log_filter)

#                 if previous == result:
#                     continue

#                 previous = result

#                 connection_info = ConnectionInfo(result)
#                 assert connection_info

#                 self._mq.publish(
#                     Topology.ChangedNotification(connection_info))
#                 log.debug("Topology changed: %s", connection_info)

#                 self._update_point_state(connection_info)

#             except Exception as ex:  # pylint: disable=W0718

#                 log.error("_worker: An exception occurred. [%s]",
#                           ex, exc_info=True)

#         log.info("_worker: Processing stopped.")

#     def get_source_point(self, name: str) -> JackAlsaSourcePoint:
#         """Creates or gets the source point with the specified name."""

#     def get_sink_point(self, name: str) -> JackAlsaSinkPoint:
#         """Creates or gets the sink point with the specified name."""
