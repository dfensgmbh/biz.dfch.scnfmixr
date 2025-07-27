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

"""Module retry."""

import time
from typing import Any, Callable

from biz.dfch.logging import log


class Retry:
    """Retries a callable until it returns True, with exponential backoff and
    attempt limit.
    """

    _spin_max_attempts: int
    _max_wait_time_ms: int
    _initial_wait_ms: int
    _max_attempts: int

    def __init__(
            self,
            spin_max_attempts: int = 10,
            max_wait_time_ms: int = 5000,
            initial_wait_time_ms: int = 150,
            max_attempts: int = 0
    ) -> None:
        """
        Initializes the retry handler.

        Args:
            wait_interval_ms: Initial wait interval in milliseconds.
            max_attempts: Maximum number of attempts. Set to 0 for unlimited
                attempts.
        """

        assert isinstance(spin_max_attempts, int) and spin_max_attempts >= 0
        assert isinstance(max_wait_time_ms, int) and max_wait_time_ms >= 0
        assert isinstance(initial_wait_time_ms,
                          int) and initial_wait_time_ms > 0
        assert isinstance(max_attempts, int) and max_attempts >= 0

        self._spin_max_attempts = spin_max_attempts
        self._max_wait_time_ms = max_wait_time_ms
        self._initial_wait_ms = initial_wait_time_ms
        self._max_attempts = max_attempts

    def invoke(
            self,
            action: Callable[..., bool],
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        Repeatedly calls `action` until it returns True or max attempts are
        exhausted.

        Args:
            action: Callable that returns a boolean.
            *args, **kwargs: Arguments to pass to the action.
        """

        assert callable(action)

        start_time = time.monotonic()
        current_wait = min(self._initial_wait_ms, self._max_wait_time_ms)
        attempts = 0
        spin_attempts = 0

        action_name = getattr(action, '__name__', type(action).__name__)
        module_name = getattr(action, '__module__', 'unknown')

        while self._max_attempts == 0 or attempts < self._max_attempts:

            try:
                elapsed_ms = int((time.monotonic() - start_time) * 1000.0)
                log.debug("Trying [%s/%s] [elapsed: %sms] ...",
                          attempts, self._max_attempts, elapsed_ms)

                if action(*args, **kwargs):
                    return

            except Exception as ex:  # pylint: disable=W0718
                log.error("An exception occurred while executing '%s.%s'. [%s]",
                          module_name,
                          action_name,
                          ex,
                          exc_info=True
                          )

            time.sleep(current_wait / 1000.0)

            attempts += 1

            if spin_attempts < self._spin_max_attempts:
                spin_attempts += 1
            else:
                current_wait = min(current_wait * 1.5, self._max_wait_time_ms)
