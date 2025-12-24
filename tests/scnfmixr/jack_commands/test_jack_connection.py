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

"""Testing JACK connections via MultiLineTextParser. Platform dependent."""

import re
import unittest

from text import MultiLineTextParser
from text import MultiLineTextParserContext


class TestJackConnection(unittest.TestCase):
    """Testing JackConnection"""

    class MyVisitor:
        """A visitor for parsing `jack_lsp` output."""

        def __init__(self):
            """Returns an instance of this object."""

            self.is_section_active = False
            self.has_section_processed = False
            self.items = []

        def process_port(self, ctx: MultiLineTextParserContext) -> bool:
            """Process the specified port.

            Args:
                ctx (MultiLineTextParserContext): The parser context.

            Returns:
                bool: True, if processing should continue; false otherwise.
            """

            assert ctx

            if 0 != ctx.level:
                return True

            self.is_section_active = True
            return True

        def process_default(self, ctx: MultiLineTextParserContext) -> bool:
            """Process any other line.

            Args:
                ctx (MultiLineTextParserContext): The parser context.

            Returns:
                bool: True, if processing should continue; false otherwise.
            """

            assert ctx

            if not self.is_section_active:
                return True

            # Stop processing after port section.
            if 0 == ctx.level:
                self.is_section_active = False
                self.has_section_processed = True
                return False

            if 1 != ctx.level:
                return True

            self.items.append(ctx.text)
            return True

    def test_parsing_port_succeeds(self):
        """Parsing a connection name succeeds."""

        text = """\
system:capture_1
system:capture_2
system:capture_3
system:capture_4
system:capture_5
system:capture_6
system:capture_7
system:capture_8
system:playback_1
system:playback_2
system:playback_3
system:playback_4
system:playback_5
system:playback_6
system:playback_7
system:playback_8
""".splitlines()

        visitor = TestJackConnection.MyVisitor()
        dic = {
            "^system:playback_": visitor.process_port,
        }

        parser = MultiLineTextParser(indent=" ", length=2, dic=dic)
        parser.parse(text, is_regex=True)

    def test_parsing_connections_succeeds(self) -> None:
        """Parsing the connections of a port succeeds."""
        text = """\
system:capture_1
system:capture_2
system:capture_3
system:capture_4
system:capture_5
system:capture_6
system:capture_7
system:capture_8
system:playback_1
system:playback_2
system:playback_3
system:playback_4
system:playback_5
system:playback_6
system:playback_7
system:playback_8
EX1-I:capture_1
   ecasound:EX1-I-DRY-I_1
EX1-I:capture_2
LCL-I:capture_1
   ecasound:LCL-I-DRY-I_1
LCL-I:capture_2
MON-O:playback_1
   ecasound:MX3-O_1
MON-O:playback_2
   ecasound:MX3-O_2
LCL-O:playback_1
   ecasound:MX0-O_1
EX2-I:capture_1
   ecasound:EX2-I-DRY-I_1
LCL-O:playback_2
   ecasound:MX0-O_2
EX2-I:capture_2
EX1-O:playback_1
   ecasound:MX1-O_1
EX2-O:playback_1
   ecasound:MX2-O_1
EX1-O:playback_2
   ecasound:MX1-O_2
EX2-O:playback_2
   ecasound:MX2-O_2
ecasound:LCL-I-DRY-I_1
   LCL-I:capture_1
ecasound:EX1-I-DRY-I_1
   EX1-I:capture_1
ecasound:EX2-I-DRY-I_1
   EX2-I:capture_1
ecasound:LCL-I-WET-I_1
   ecasound:LCL-I-DRY-O_1
ecasound:EX1-I-WET-I_1
   ecasound:EX1-I-DRY-O_1
ecasound:EX2-I-WET-I_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX0-I_1
   ecasound:EX1-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX0-I_2
   ecasound:EX1-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX1-I_1
   ecasound:LCL-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX1-I_2
   ecasound:LCL-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX2-I_1
   ecasound:LCL-I-DRY-O_1
   ecasound:EX1-I-DRY-O_1
ecasound:MX2-I_2
   ecasound:LCL-I-DRY-O_1
   ecasound:EX1-I-DRY-O_1
ecasound:MX3-I_1
   ecasound:LCL-I-DRY-O_1
   ecasound:EX1-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX3-I_2
   ecasound:LCL-I-DRY-O_1
   ecasound:EX1-I-DRY-O_1
   ecasound:EX2-I-DRY-O_1
ecasound:MX4-I_1
   ecasound:LCL-I-DRY-O_1
ecasound:MX4-I_2
   ecasound:LCL-I-WET-O_1
ecasound:MX4-I_3
   ecasound:EX1-I-DRY-O_1
ecasound:MX4-I_4
   ecasound:EX1-I-WET-O_1
ecasound:MX4-I_5
   ecasound:EX2-I-DRY-O_1
ecasound:MX4-I_6
   ecasound:EX2-I-WET-O_1
ecasound:LCL-I-DRY-O_1
   ecasound:LCL-I-WET-I_1
   ecasound:MX1-I_1
   ecasound:MX1-I_2
   ecasound:MX2-I_1
   ecasound:MX2-I_2
   ecasound:MX3-I_1
   ecasound:MX3-I_2
   ecasound:MX4-I_1
ecasound:EX1-I-DRY-O_1
   ecasound:EX1-I-WET-I_1
   ecasound:MX0-I_1
   ecasound:MX0-I_2
   ecasound:MX2-I_1
   ecasound:MX2-I_2
   ecasound:MX3-I_1
   ecasound:MX3-I_2
   ecasound:MX4-I_3
ecasound:EX2-I-DRY-O_1
   ecasound:EX2-I-WET-I_1
   ecasound:MX0-I_1
   ecasound:MX0-I_2
   ecasound:MX1-I_1
   ecasound:MX1-I_2
   ecasound:MX3-I_1
   ecasound:MX3-I_2
   ecasound:MX4-I_5
ecasound:LCL-I-WET-O_1
   ecasound:MX4-I_2
ecasound:EX1-I-WET-O_1
   ecasound:MX4-I_4
ecasound:EX2-I-WET-O_1
   ecasound:MX4-I_6
ecasound:MX0-O_1
   LCL-O:playback_1
ecasound:MX0-O_2
   LCL-O:playback_2
ecasound:MX1-O_1
   EX1-O:playback_1
ecasound:MX1-O_2
   EX1-O:playback_2
ecasound:MX2-O_1
   EX2-O:playback_1
ecasound:MX2-O_2
   EX2-O:playback_2
ecasound:MX3-O_1
   MON-O:playback_1
ecasound:MX3-O_2
   MON-O:playback_2
ecasound:MX4-O_1
ecasound:MX4-O_2
ecasound:MX4-O_3
ecasound:MX4-O_4
ecasound:MX4-O_5
ecasound:MX4-O_6
""".splitlines()

        visitor = TestJackConnection.MyVisitor()
        dic = {
            f"^{re.escape('ecasound:MX0-I_2')}": visitor.process_port,
        }

        parser = MultiLineTextParser(
            indent=" ",
            length=3,
            dic=dic,
            default=visitor.process_default)
        parser.parse(text, is_regex=True)

        result = visitor.items
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "ecasound:EX1-I-DRY-O_1")
        self.assertEqual(result[1], "ecasound:EX2-I-DRY-O_1")
