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

"""Module time_conversion."""

import math

from biz.dfch.logging import log


class TimeConversion:
    """Conversion functions for time monotonic."""

    _frames_per_second = 75
    _flac_frame_size: int = 4096

    _initial_value: float
    _sample_rate: int
    _cue_frame_size: int
    _lcm: int

    @staticmethod
    def _get_lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    def __init__(self, value: float, sample_rate: int = 48000):

        assert isinstance(value, float) and 0 <= value
        assert isinstance(sample_rate, int) and 0 <= sample_rate

        self._initial_value = value
        self._sample_rate = sample_rate
        assert 0 == (sample_rate % self._frames_per_second)
        self._cue_frame_size = int(sample_rate / self._frames_per_second)

        # We need the least common multiplier of both the FLAC frame size
        # (which is fixed at 4096). And the cue sheet fps (based on the sampling
        # rate). This will be 20480 for 48000Hz.
        self._lcm = TimeConversion._get_lcm(
            self._flac_frame_size, self._cue_frame_size)

        log.debug("[cue_frame_size: '%s'] [lcm '%s'] [sample_rate '%s']",
                  self._cue_frame_size, self._lcm, self._sample_rate)

    def get_isotime_from_sample(self, value: int) -> str:
        """Returns the iso time HH:mm:ss from the specified sample."""

        _seconds_per_hour: int = 3600
        _seconds_per_minute: int = 60
        assert isinstance(value, int) and 0 <= value

        total_seconds = int(value / self._sample_rate)

        hours, remainer = divmod(total_seconds, _seconds_per_hour)
        minutes, remainder = divmod(remainer, _seconds_per_minute)
        seconds = int(remainder)

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_samples_aligned(self, value: float) -> int:
        """Returns number of samples (from initial_value to value), floored to
        nearest multiple of _lcm."""

        assert isinstance(value, float) and value >= self._initial_value

        total_samples = int((value - self._initial_value) * self._sample_rate)

        result = (total_samples // self._lcm) * self._lcm

        return result

    def to_cuesheet_string(self, value: float) -> str:
        """Returns an mm:ss:ff time string representing the delta of
        initial_value and value.

        Parameters:
            value (float): Time in seconds (can be fractional).

        Returns:
            str: Time string in mm:ss:ff format (ff := frames at 75fps).
        """

        _seconds_per_minute = 60

        assert isinstance(value, float) and value >= self._initial_value

        samples_aligned = self.get_samples_aligned(value)
        total_seconds = samples_aligned / self._sample_rate

        minutes, remainder = divmod(total_seconds, _seconds_per_minute)
        minutes = int(minutes)
        seconds = int(remainder)
        frames = int(remainder % 1 * self._frames_per_second)

        result = f"{minutes:02}:{seconds:02}:{frames:02}"

        return result
