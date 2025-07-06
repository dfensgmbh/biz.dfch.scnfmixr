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

"""Module app_ctx."""

import threading

from typing import final

from .app import LanguageCode
from .name_input import DateTimeNameInput


@final
class ApplicationContext():
    """Global ApplicationContext."""

    _instance = None
    _lock = threading.Lock()

    @property
    def language(self) -> LanguageCode:
        """The currently active language."""

        return self._language

    @language.setter
    def language(self, value: LanguageCode) -> None:

        assert value and isinstance(value, LanguageCode)

        self._language = value

    def __str__(self) -> str:
        result = {
            "language": self._language
        }

        return str(result)

    def __new__(cls):
        """Thread safe instance creation."""

        if cls._instance:
            return cls._instance

        with cls._lock:

            if not cls._instance:

                cls._instance = super().__new__(cls)

                # Set default values here and not in __init__.
                cls._instance.language = LanguageCode.EN
                cls.date_string = ""
                cls.date_time_name_input = DateTimeNameInput()

        return cls._instance
