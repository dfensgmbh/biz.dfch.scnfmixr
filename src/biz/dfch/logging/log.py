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

import os
import sys

import logging
import logging.config

_LOGGER_NAME = "biz.dfch.scnfmix"
# Note: When using `pyinstaller --onefile` make sure this file is available.
_LOGGER_FILE = "logging.conf"


def resolve_resource_file(path: str) -> str:
    """Resolves a relative path to the runtime path."""

    assert path

    if getattr(sys, "frozen", False):
        # Determine whether we run as binary onefile.
        base_path = sys._MEIPASS  # pylint: disable=W0212
    else:
        base_path = os.getcwd()

    return os.path.join(base_path, path)


try:
    print(f"{__file__} - {__name__}")
    print(f"path     '{_LOGGER_FILE}'")
    print(f"resolved '{resolve_resource_file(_LOGGER_FILE)}'")

    logging.config.fileConfig(resolve_resource_file(_LOGGER_FILE))
    log = logging.getLogger(_LOGGER_NAME)
    log.debug("Logging configuration initialised from '%s'.",
              _LOGGER_FILE)

except Exception as ex:

    print(f"{_LOGGER_NAME}: An error occurred while trying to load "
          f"'{_LOGGER_FILE}': '{ex}'")

    raise
