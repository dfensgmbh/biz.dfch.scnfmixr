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
        """Gets the raw ALSA device name."""

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
