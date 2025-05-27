# test_main.py

import os
import sys
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
