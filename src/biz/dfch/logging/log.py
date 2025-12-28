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

"""Module log"""

import logging
import logging.config

from biz.dfch.i18n import I18n

_LOGGER_NAME = "biz.dfch.scnfmixr"
# Note: When using `pyinstaller --onefile` make sure this file is available.
_LOGGER_FILE = "logging.conf"


try:
    logging.config.fileConfig(I18n.Factory.get().get_runtime_path(_LOGGER_FILE))
    log = logging.getLogger(_LOGGER_NAME)
    log.debug("Logging configuration initialized from '%s'.",
              _LOGGER_FILE)

except Exception as ex:

    print(f"{_LOGGER_NAME}: An error occurred while trying to load "
          f"'{_LOGGER_FILE}': '{ex}'")

    raise
