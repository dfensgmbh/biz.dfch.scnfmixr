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

# pylint: disable=C0112,C0116
# mypy: disable-error-code=annotation-unchecked

"""TestResSndFiles"""

import unittest

from pathlib import Path


import biz.dfch.scnfmixr as scnfmixr


class TestResSndFiles(unittest.TestCase):
    """Examine resource wave sound files."""

    res_dir = "res"
    src_lang = "en"

    def _get_filenames(self, path: Path) -> set[str]:
        result = {
            p.name for p
            in path.iterdir()
            if p.is_file()
        }
        return result
    
    def _test_lang_extra(self, lang: str):
        base_path = Path(scnfmixr.__file__).resolve().parent
        left_path: Path = base_path / self.res_dir / self.src_lang
        right_path: Path = base_path / self.res_dir / lang

        print(left_path)
        print(right_path)
        files_left = self._get_filenames(left_path)
        files_right = self._get_filenames(right_path)

        extra = files_right - files_left

        self.assertFalse(
            extra,
            f"[{len(files_left)}:{len(files_right)}:{len(extra)}] "
            f"[{lang}] "
            f"Extra files: [{sorted(extra)}]"
        )

    def _test_lang_missing(self, lang: str):
        base_path = Path(scnfmixr.__file__).resolve().parent
        left_path: Path = base_path / self.res_dir / self.src_lang
        right_path: Path = base_path / self.res_dir / lang

        print(left_path)
        print(right_path)
        files_left = self._get_filenames(left_path)
        files_right = self._get_filenames(right_path)

        missing = files_left - files_right

        self.assertFalse(
            missing,
            f"[{len(files_left)}:{len(files_right)}:{len(missing)}] "
            f"[{lang}] "
            f"Missing files: [{sorted(missing)}]"
        )

    def test_de_extra(self):
        """Examine resource EN and DE wave sound files."""

        lang = "de"
        self._test_lang_extra(lang)

    def test_de_missing(self):
        """Examine resource EN and DE wave sound files."""

        lang = "de"
        self._test_lang_missing(lang)

    def test_fr_extra(self):
        """Examine resource EN and FR wave sound files."""

        lang = "fr"
        self._test_lang_extra(lang)

    def test_fr_missing(self):
        """Examine resource EN and FR wave sound files."""

        lang = "fr"
        self._test_lang_missing(lang)

    def test_it_extra(self):
        """Examine resource EN and IT wave sound files."""

        lang = "it"
        self._test_lang_extra(lang)

    def test_it_missing(self):
        """Examine resource EN and IT wave sound files."""

        lang = "it"
        self._test_lang_missing(lang)
