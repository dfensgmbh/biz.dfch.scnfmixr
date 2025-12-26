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

"""Module thread_pool."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, ClassVar
import threading

from biz.dfch.logging import log


class ThreadPool:  # pylint: disable=R0903
    """Implements a simple thread pool."""

    MAX_WORKERS: int = 4

    _executor: ThreadPoolExecutor

    def __init__(self, max_workers: int):

        if not ThreadPool.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert isinstance(
            max_workers, int) and ThreadPool.MAX_WORKERS >= max_workers

        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        DEFAULT_WORKERS: int = 2

        DEFAULT_NAME = "default"

        __thread_pools: ClassVar[dict[str, ThreadPool]] = {}

        __instance: ClassVar[ThreadPool | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

        @staticmethod
        def get(
            name: str = DEFAULT_NAME,
            max_workers: int = DEFAULT_WORKERS
        ) -> ThreadPool:
            """Creates or gets a named thread pool instance."""

            assert isinstance(name, str) and name.strip()
            assert isinstance(
                max_workers, int) and ThreadPool.MAX_WORKERS >= max_workers

            with ThreadPool.Factory._sync_root:

                result = ThreadPool.Factory.__thread_pools.get(name, None)
                if result is not None:
                    return result

                result = ThreadPool(max_workers=max_workers)

                ThreadPool.Factory.__thread_pools[name] = result

                return result

    @staticmethod
    def _action_invoker(func: Callable, *args: Any, **kwargs: Any) -> None:

        try:
            func(*args, **kwargs)

        except Exception as ex:  # pylint: disable=W0718
            log.error("An exception occurred. [%s]", ex, exc_info=True)

    def invoke(self, action: Callable, *args: Any, **kwargs: Any) -> None:
        """Executes an action on the thread pool.."""

        self._executor.submit(self._action_invoker, action, *args, **kwargs)
