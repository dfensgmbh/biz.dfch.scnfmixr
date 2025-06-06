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

import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.Text.TextUtils import TextUtils
from src.__main__ import get_usbid


class MainTest(unittest.TestCase):

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
            MagicMock(__enter__=lambda s: MagicMock(readline=lambda: expected_idVendor)),
            MagicMock(__enter__=lambda s: MagicMock(readline=lambda: expected_idProduct)),
        ]
        # Act
        result = get_usbid("arbitrary-usb-id")

        # Assert
        self.assertEqual(result, f"{expected_idVendor}:{expected_idProduct}")
        self.assertEqual(mock_os_path_isfile.call_count, 2)
        self.assertEqual(mock_builtins_open.call_count, 2)


if __name__ == "__main__":
    unittest.main()
