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

"""Module connection_parameters."""

from dataclasses import dataclass

from .constant import Constant


@dataclass(frozen=True)
class Connection:
    """Parameters for a routing entry."""

    this: str
    other: str
    idx_this: int = 0
    idx_other: int = 0

    @staticmethod
    def source(value: str) -> str:
        """Gets the source name of the specified value."""

        assert value and value.strip()

        input_suffix = f"{Constant.JACK_INFIX}{Constant.JACK_INPUT}"

        if value.endswith(input_suffix):
            return value

        return f"{value}{input_suffix}"

    @staticmethod
    def sink(value: str) -> str:
        """Gets the sink name of the specified value."""

        assert value and value.strip()

        output_suffix = f"{Constant.JACK_INFIX}{Constant.JACK_OUTPUT}"

        if value.endswith(output_suffix):
            return value

        return f"{value}{output_suffix}"

    @staticmethod
    def jack_client_name_source_prefix(value: str) -> str:
        """Returns 'Alsa:<value>-I'."""

        result = (f"{Constant.JACK_ALSA_PREFIX}"
                  f"{Constant.JACK_SEPARATOR}"
                  f"{value}"
                  f"{Constant.JACK_INFIX}"
                  f"{Constant.JACK_INPUT}")
        return result

    @staticmethod
    def jack_client_name_sink_prefix(value: str) -> str:
        """Returns 'Alsa:<value>-I'."""

        result = (f"{Constant.JACK_ALSA_PREFIX}"
                  f"{Constant.JACK_SEPARATOR}"
                  f"{value}"
                  f"{Constant.JACK_INFIX}"
                  f"{Constant.JACK_OUTPUT}")
        return result
