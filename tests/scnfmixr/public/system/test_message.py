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

"""Module test_message."""

from __future__ import annotations
import unittest
from biz.dfch.scnfmixr.public.system.message_base import Message
from biz.dfch.scnfmixr.public.system.message_base import MessageHigh
from biz.dfch.scnfmixr.public.system.message_base import MessageMedium
from biz.dfch.scnfmixr.public.system.message_base import MessageLow


class TestMessage(unittest.TestCase):
    """Class testing template."""

    class MyMessage(Message):
        """Priority Medium."""

    class ArbitraryMessageHigh(MessageHigh):
        """Priority High."""

        description: str

        def __init__(self, description: str):
            super().__init__(
                TestMessage.ArbitraryMessageHigh.__qualname__)

            assert description and description.strip()

            self.description = description

    class ArbitraryMessageMedium(MessageMedium):
        """Priority Medium."""

    class ArbitraryMessageLow(MessageLow):
        """Priority Low."""

    def test_qualname(self):
        """Testing qualname."""

        sut = TestMessage.ArbitraryMessageHigh

        self.assertIsNotNone(sut)

        result = sut.name

        self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()
