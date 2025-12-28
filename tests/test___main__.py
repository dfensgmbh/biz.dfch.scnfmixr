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

import unittest
from unittest.mock import MagicMock, mock_open, patch

from text import TextUtils
from biz.dfch.scnfmixr.audio import Usb


class MainTest(unittest.TestCase):
    """Test __main__.py."""

    # Arrange
    expected_builtins_open = "This is a mock file content"

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=expected_builtins_open)
    def test_read_first_file(self, mock_builtin_opens, mock_os_path_isfile):

        # Act
        result = TextUtils().read_first_line("arbitrary_file.txt")

        # Assert
        self.assertEqual(result, self.expected_builtins_open)

        mock_os_path_isfile.assert_called_once_with("arbitrary_file.txt")
        mock_builtin_opens.assert_called_once_with("arbitrary_file.txt", "r")

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=expected_builtins_open)
    def test_get_usbid_returns_usbid(self, mock_builtins_open, mock_os_path_isfile):

        expected_idVendor = "1234"
        expected_idProduct = "ABCD"
        mock_builtins_open.side_effect = [
            MagicMock(__enter__=lambda s: MagicMock(
                readline=lambda: expected_idVendor)),
            MagicMock(__enter__=lambda s: MagicMock(
                readline=lambda: expected_idProduct)),
        ]
        # Act
        result = Usb.get_usbid("arbitrary-usb-id")

        # Assert
        self.assertEqual(result, f"{expected_idVendor}:{expected_idProduct}")
        self.assertEqual(mock_os_path_isfile.call_count, 2)
        self.assertEqual(mock_builtins_open.call_count, 2)


if __name__ == "__main__":
    unittest.main()
