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

"""Module signal_path_lazy_manager."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, ClassVar
import threading

from biz.dfch.logging import log


class ThreadPool:
    """Implements a simple thread pool."""

    _executor: ThreadPoolExecutor

    def __init__(self, max_workers: int = 4):

        if not ThreadPool.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert 1 < max_workers <= 4

        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    class Factory:  # pylint: disable=R0903
        """Factory class."""

        __instance: ClassVar[ThreadPool | None] = None
        _sync_root: ClassVar[threading.Lock] = threading.Lock()

        @staticmethod
        def get() -> ThreadPool:
            """Creates or gets signal path instances."""

            if ThreadPool.Factory.__instance is not None:
                return ThreadPool.Factory.__instance

            with ThreadPool.Factory._sync_root:

                if ThreadPool.Factory.__instance is not None:
                    return ThreadPool.Factory.__instance

                ThreadPool.Factory.__instance = (
                    ThreadPool()
                )

            return ThreadPool.Factory.__instance

    @staticmethod
    def _action_invoker(func: Callable, *args: Any, **kwargs: Any) -> None:

        try:
            func(*args, **kwargs)

        except Exception as ex:  # pylint: disable=W0718
            log.error("An exception occurred. [%s]", ex, exc_info=True)

    def invoke(self, action: Callable, *args: Any, **kwargs: Any) -> None:
        """Executes an action on the thread pool.."""

        self._executor.submit(self._action_invoker, action, *args, **kwargs)
