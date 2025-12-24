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

"""Module media_player_command."""

from enum import StrEnum


class MediaPlayerCommand(StrEnum):
    """Media Player Client commands."""

    UPDATE = "update"
    STATUS = "status"
    LIST_AUDIO = "listall"
    LOAD = "load"
    CLEAR = "clear"
    ADD = "add"
    PLAYLIST = "playlist"
    REPEAT = "repeat"
    CONSUME = "consume"
    SINGLE = "single"
    RANDOM = "random"
    START = "play"
    STOP = "stop"
    PAUSE = "pause"
    NEXT = "next"
    PREVIOUS = "prev"
    SEEK = "seek"
