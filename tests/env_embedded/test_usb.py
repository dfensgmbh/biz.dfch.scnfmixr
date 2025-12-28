# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
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

"""Module test_usb."""

import unittest
from unittest.mock import mock_open, patch

from biz.dfch.scnfmixr.audio import Usb


class TestUsb(unittest.TestCase):
    """TestUsb"""

    # Arrange
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open,
           read_data="This is a mock file content")
    def test_get_usbid_returns_usbid(
            self,
            mock_builtins_open,
            mock_os_path_isfile
    ):
        """Testing returned usb_id."""

        expected_vendor_id = "1234"
        expected_product_id = "ABCD"
        mock_builtins_open.side_effect = [
            mock_open(read_data=expected_vendor_id).return_value,
            mock_open(read_data=expected_product_id).return_value,
        ]

        # Act
        result = Usb.get_usbid("arbitrary-usb-id")

        # Assert
        self.assertEqual(result, f"{expected_vendor_id}:{expected_product_id}")
        self.assertEqual(mock_os_path_isfile.call_count, 2)
        self.assertEqual(mock_builtins_open.call_count, 2)

    def test_get_usbid_with_empty_id_throws(self):
        """An empty id throws."""

        with self.assertRaises(AssertionError):
            Usb.get_usbid(None)
