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


from dataclasses import dataclass

__all__ = ["MultiLineTextParserContext"]


@dataclass
class MultiLineTextParserContext:
    """Provides context for the `MultiLineTextParser`.
    Attributes:
        line (int): Line number in the source text.
        level (int): Hierarchical level of current line (start at 0).
        levelPrevious (int): Hierarchical level of previous line.
        keyword (str): The current keyword being parsed.
        text (str): Associated text including the keyword.
    """

    line: int = 0
    level: int = 0
    level_previous: int = 0
    keyword: str = None
    text: str = None
