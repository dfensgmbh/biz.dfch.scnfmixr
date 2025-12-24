# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
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

"Module ui_parameters."

from __future__ import annotations
from enum import StrEnum, auto

from biz.dfch.i18n import LanguageCode


# pylint: disable=R0903
class UiParameters:
    """UI parameters for the application."""

    class Keys(StrEnum):
        """Keys in this class."""

        LANGUAGE = auto()

    language: LanguageCode

    def __init__(self):
        self.language = LanguageCode.DEFAULT

    def __str__(self) -> str:

        result = {
            "language": self.language
        }

        return str(result)

    def __repr__(self) -> str:
        return self.__str__()
