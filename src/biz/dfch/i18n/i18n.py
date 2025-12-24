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

"""Module i18n."""

from __future__ import annotations
import os
from pathlib import Path
import sys
from threading import Lock
from typing import ClassVar

from .language_code import LanguageCode


class I18n:
    """Internationalisation module."""

    _RES_PATH = "res"

    _path: str

    def __init__(self, value: str):

        if not I18n.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert value is not None and isinstance(value, str)

        self._path = value

    class Factory:  # pylint: disable=R0903
        """Factory class for creating `I18n` instances."""

        __instance: ClassVar[I18n | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def _reset(value: str | None = None) -> None:
            """Internal: Reset the initial value of the path."""

            assert I18n.Factory.__instance

            if not value:
                value = ""

            with I18n.Factory._sync_root:
                I18n._path = value  # pylint: disable=W0212

        @staticmethod
        def create(value: str | None = None) -> I18n:
            """Creates the `I18n` singleton instance.

            Args:
                value (str | None): A relative path, "" or None. Default is
                    `None`.

            Returns:
                I18: An instance of the object.

            Raises:
                AssertionError: If the instance has already been created.
            """

            assert not I18n.Factory.__instance

            if not value:
                value = ""

            with I18n.Factory._sync_root:
                assert not I18n.Factory.__instance

                I18n.Factory.__instance = I18n(value)

            return I18n.Factory.__instance

        @staticmethod
        def get() -> I18n:
            """Returns the `I18n` singleton instance.

            Returns:
                I18: An instance of the object.

            Raises:
                AssertionError: If the instance has not been created.
            """

            assert I18n.Factory.__instance

            return I18n.Factory.__instance

    def get_runtime_path(self, relative_path: str) -> str:
        """Resolves a relative path to the runtime path.

        Args:
            relative_path (str): The relative (to __main__.py) path to
                translate.

        Returns:
            str: The runtime path depending on the environment (frozen or
                source).

        Raises:
            AssertionError: If relative_path is None or "".
        """

        assert relative_path and relative_path.strip()

        if getattr(sys, "frozen", False):
            # Determine whether we run as binary "onefile".
            base_path = getattr(sys, "_MEIPASS", None)
            assert base_path
        else:
            base_path = os.path.join(os.getcwd(), self._path)

        return os.path.normpath(os.path.join(base_path, relative_path))

    def get_resource_path(
            self,
            item: str,
            code: LanguageCode | None = None
    ) -> str:
        """Returns the normalised resource path for an item.

        Args:
            item (str): The item to join with the _RES_PATH.
            code (LanguageCode | None): If specified, the language code will be
                infixed as a sub directory under _RES_PATH

        Returns:
            str: The normalised path (without resolving links).

        Raises:
            AssertionError: If item is None or "".
        """

        assert item and item.strip()

        path = Path(item)

        if code is not None:
            if code is LanguageCode.DEFAULT:
                code = LanguageCode.EN
            result = os.path.join(I18n._RES_PATH, code.name, path)
        else:
            result = os.path.join(I18n._RES_PATH, path)

        return self.get_runtime_path(result)
