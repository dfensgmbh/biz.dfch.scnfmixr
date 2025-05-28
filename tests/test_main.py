# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH

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
from unittest import mock
from unittest.mock import patch

from src.main import read_first_line
from src.main import get_usbid


class TestReadFirstLine(unittest.TestCase):

    # Arrange
    expected = "This is a mock file content"

    @mock.patch("builtins.open", mock.mock_open(read_data=expected))
    def test_read_first_file(self):
        # Act
        result = read_first_line("arbitrary_file.txt")
        # Assert
        self.assertEqual(result, self.expected)

    # Arrange
    @patch('src.main.read_first_line')
    def test_get_usbid_returns_usbid(self, mock_read):
        expected_idVendor = '1234'
        expected_idProduct = 'ABCD'
        mock_read.side_effect = [
            expected_idVendor,
            expected_idProduct
        ]

        # Act
        result = get_usbid('arbitrary-usb-id')

        # Assert
        self.assertEqual(result, f'{expected_idVendor}:{expected_idProduct}')
        self.assertEqual(mock_read.call_count, 2)


if __name__ == "__main__":
    unittest.main()
