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

"""Module detecting_hi2_worker."""

from StreamDeck.DeviceManager import DeviceManager   # type: ignore

from biz.dfch.logging import log

from ..interface_detector_base import InterfaceDetectorBase

from ...public.ui.streamdeck_type import StreamdeckType


# pylint: disable=R0903
class DetectingHi2Worker(InterfaceDetectorBase):
    """Implements the logic from `DetectingH2`."""

    _value: str

    def __init__(self, value: str):
        super().__init__()

        assert value and value.strip()

        self._value = value

    def select(self) -> str | None:
        """
        Selects the first matching Streamdeck based on the USB path and
        returns the index of the device.

        Note:
            The Streamdeck must be a Streamdeck MK.2.

        Returns:
            str: The Streamdeck index.
        """

        result: str | None = None
        decks = DeviceManager().enumerate()
        log.debug("Streamdecks found: '%s'.", len(decks))
        for index, deck in enumerate(decks):

            product_id = deck.product_id()
            usb_path = deck.id()

            log.debug(
                "[%s] '%s': ProductId '0x%04x'. Path '%s' (expected '%s').",
                index,
                deck.deck_type(),
                product_id,
                usb_path,
                self._value
            )

            if not usb_path.startswith(self._value):
                continue

            if StreamdeckType.ORIGINAL_MK2 != product_id:
                continue

            log.info("[%s] Selected Streamdeck: '%s'.", index, type(deck))

            result = str(index)
            break

        return result
