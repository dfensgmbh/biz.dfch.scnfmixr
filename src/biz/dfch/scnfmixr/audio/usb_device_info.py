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

from dataclasses import dataclass

__all__ = ["UsbDeviceInfo"]


@dataclass(frozen=True)
class UsbDeviceInfo:
    """Contains information about a USB device.

    Attributes:
        manufacturer (str): The manfacturer name of the device.
        product (str): The product name of the device.
        version (str | None): The version of the device.
        id_vendor (str): The USB vendor id ('abcd').
        id_product (str): The USB product id ('1234').
        busnum (str): The USB bus number.
        devnum (str): The USB device number (increments between reconnects per
            bus).
    """

    manufacturer: str
    product: str
    version: str | None
    id_vendor: str
    id_product: str
    busnum: int
    devnum: int
