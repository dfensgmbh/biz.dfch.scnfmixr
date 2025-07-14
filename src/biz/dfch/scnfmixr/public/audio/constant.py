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

"""Package constant."""

from enum import StrEnum


class Constant(StrEnum):
    """ALSA constants."""

    ALSA_DEVICE_PREFIX = "hw:"
    ALSA_CARD_PREFIX = "CARD="
    ALSA_NAME_SEPARATOR = ","
    ALSA_INTERFACE_PREFIX = "DEV="
    ALSA_NAME_INTERFACE = "0"

    @staticmethod
    def get_raw_device_name(
            card_id: str | int,
            interface_id: str | int = 0
    ) -> str:
        """Gets the raw ALSA device name"""

        assert (
            isinstance(card_id, str) and card_id.isdigit() or
            (isinstance(card_id, int) and 0 <= card_id)
        )

        assert (
            isinstance(interface_id, str) and interface_id.isdigit() or
            (isinstance(interface_id, int) and 0 <= interface_id)
        )

        card_id = int(card_id)
        interface_id = int(interface_id)

        result = (
            f"{Constant.ALSA_DEVICE_PREFIX}"
            f"{Constant.ALSA_CARD_PREFIX}"
            f"{card_id}"
            f"{Constant.ALSA_NAME_SEPARATOR}"
            f"{Constant.ALSA_INTERFACE_PREFIX}"
            f"{interface_id}"
        )

        return result
