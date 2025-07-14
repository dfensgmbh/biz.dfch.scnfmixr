# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

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
