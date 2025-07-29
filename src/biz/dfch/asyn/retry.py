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

    _initial_wait_time_ms: int
    _first_wait_time_ms: int
    _max_wait_time_ms: int
    _factor_wait_time_interval: float
    _spin_attempts: int
    _max_wait_time_ms: int
    _base_wait_time_interval_ms: int
    _max_attempts: int
    _description: str

    def __init__(
            self,
            initial_wait_time_ms: int = 0,
            first_wait_time_ms: int = 0,
            max_wait_time_ms: int = 60000,
            spin_attempts: int = 10,
            base_wait_time_interval_ms: int = 150,
            max_wait_time_interval_ms: int = 5000,
            factor_wait_time_interval: float = 1.5,
            max_attempts: int = 0,
            description: str = "",
    ) -> None:
        """
        Initializes the retry handler.

        Args:
            wait_interval_ms: Initial wait interval in milliseconds.
            max_attempts: Maximum number of attempts. Set to 0 for unlimited
                attempts.
        """

        assert isinstance(initial_wait_time_ms,
                          int) and initial_wait_time_ms >= 0
        assert isinstance(first_wait_time_ms,
                          int) and first_wait_time_ms >= 0
        assert isinstance(max_wait_time_ms,
                          int) and max_wait_time_ms >= 0
        assert isinstance(factor_wait_time_interval,
                          float) and factor_wait_time_interval >= 0
        assert isinstance(spin_attempts, int) and spin_attempts >= 0
        assert isinstance(max_wait_time_interval_ms, int) \
            and max_wait_time_interval_ms >= 0
        if 0 != max_wait_time_interval_ms:
            assert initial_wait_time_ms \
                + first_wait_time_ms \
                <= max_wait_time_interval_ms
        assert isinstance(base_wait_time_interval_ms,
                          int) and base_wait_time_interval_ms > 0
        assert isinstance(max_attempts, int) and max_attempts >= 0

        self._initial_wait_time_ms = initial_wait_time_ms
        self._first_wait_time_ms = first_wait_time_ms
        self._max_wait_time_ms = max_wait_time_ms
        self._factor_wait_time_interval = factor_wait_time_interval
        self._spin_attempts = spin_attempts
        self._max_wait_time_ms = max_wait_time_interval_ms
        self._base_wait_time_interval_ms = base_wait_time_interval_ms
        self._max_attempts = max_attempts
        self._description = description

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

        action_name = getattr(action, '__name__', type(action).__name__)
        module_name = getattr(action, '__module__', 'unknown')

        if self._description is None or not self._description.strip():
            self._description = f"{module_name}.{action}"

        attempts = 0
        spin_attempts = 0

        current_wait = min(self._base_wait_time_interval_ms,
                           self._max_wait_time_ms)
        start_time = time.monotonic()

        if 0 < self._initial_wait_time_ms:
            time.sleep(self._initial_wait_time_ms / 1000.0)

        while self._max_attempts == 0 or attempts < self._max_attempts:

            try:
                elapsed_ms = int((time.monotonic() - start_time) * 1000.0)
                if elapsed_ms > self._max_wait_time_ms:
                    break

                log.debug("Trying '%s' [%s/%s] [elapsed: %sms] ...",
                          self._description,
                          attempts,
                          self._max_attempts,
                          elapsed_ms)

                if action(*args, **kwargs):
                    return

                if 0 == attempts and 0 < self._first_wait_time_ms:
                    time.sleep(self._first_wait_time_ms / 1000.0)

            except Exception as ex:  # pylint: disable=W0718
                log.error("An exception occurred while executing "
                          "'%s' in '%s.%s'. [%s]",
                          self._description,
                          module_name,
                          action_name,
                          ex,
                          exc_info=True
                          )

            finally:
                time.sleep(current_wait / 1000.0)

                attempts += 1

                if spin_attempts < self._spin_attempts:
                    spin_attempts += 1
                else:
                    current_wait = min(
                        current_wait * self._factor_wait_time_interval,
                        self._max_wait_time_ms)
