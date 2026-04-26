# Copyright (c) 2025-2026 d-fens GmbH, http://d-fens.ch
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

"""Module args."""

import argparse
from dataclasses import dataclass
import re

from biz.dfch.i18n import LanguageCode
from .public import SKIP_USB_PORT
from .public.audio import AudioDevice
from .public.audio import FileFormat
from .public.audio import Format
from .public.audio import SampleRate
from .public.input import InputDevice
from .public.input import MenuProfile
from .public.mixer import MixbusDevice
from .public.storage import StorageDevice


__all__ = [
    "Arguments",
]


@dataclass(frozen=True)
class Arguments():
    """Define programme arguments.

    Attributes:
        prog_name (str): The programme name.
        version (str): The programme version.
    """

    prog_name: str
    version: str

    def __postinit__(self):

        assert self.prog_name and self.prog_name.strip()
        assert self.version and self.version.strip()

    def _validate_hex_string(self, value: str) -> str:
        """Validates the specified value.

        Args:
            value (str): The value to validate. Must be of the following
                format: '^[0-9a-fA-F]{4}(:[0-9a-fA-F]{4})?$'
        Returns:
            str: The unmodified value.

        Raises:
            ArgumentTypeError: If the specified value is not a valid hex
                string.
        """

        if re.fullmatch(r'^[0-9a-fA-F]{4}(:[0-9a-fA-F]{4})?$', value):
            return value

        raise argparse.ArgumentTypeError(
            f"'{value}' is not valid. Format: "
            f"'^[0-9a-fA-F]{4}(:[0-9a-fA-F]{4})?$'.")

    def _validate_record_targets(self, value: str) -> str:
        valid_keys = [e.name for e in MixbusDevice]
        if value not in valid_keys:
            raise argparse.ArgumentTypeError(
                f"Invalid mixbus device '{value}'. "
                f"Valid options: {', '.join(valid_keys)}"
            )
        return value

    def get(self) -> argparse.Namespace:
        """Returns an instance to the argument parser.

        Returns:
            argparse.Namespace: The namespace of the parsed arguments.
        """

        # pylint: disable=C0301
        description = f"""%(prog)s (Secure Conference Mixer and Recorder), v{self.version}

Copyright 2024-2026 d-fens GmbH. Licensed under GPLv3.
"""  # noqa: E501

        # Process command line arguments.
        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=("For more information see "
                    "https://github.com/dfensgmbh/biz.dfch.scnfmixr/."),
        )

        parser.add_argument(
            "--version", "-v",
            action="version",
            version=f"%(prog)s, v{self.version}",
        )
        parser.add_argument(
            "--service", "-s",
            action="store_true",
            help="Run %(prog)s as service.",
        )
        parser.add_argument(
            "--language", "-l",
            type=str,
            choices=[
                LanguageCode.DEFAULT,
                LanguageCode.EN.name,
                LanguageCode.DE.name,
                LanguageCode.FR.name,
                LanguageCode.IT.name,
            ],
            default=LanguageCode.DEFAULT.name,
            help="Select the user interface language.",
        )
        parser.add_argument(
            "--use-current-date", "-cd",
            action="store_true",
            help="Use current date.",
        )
        parser.add_argument(
            "--use-current-time", "-ct",
            action="store_true",
            help="Use current time.",
        )
        parser.add_argument(
            "--use-random-name", "-rn",
            action="store_true",
            help="Use pseudo-random name.",
        )

        # Profile.
        parser.add_argument(
            "--profile", "-p",
            type=str,
            choices=[
                MenuProfile.DEFAULT.name,
                MenuProfile.RECORDER.name,
                MenuProfile.PLAYBACK.name,
            ],
            default=MenuProfile.DEFAULT.name,
            help="Select menu profile for user interface.",
        )

        # Audio format and audio parameters.
        parser.add_argument(
            "--file-format", "-ff",
            type=str,
            choices=[
                FileFormat.DEFAULT.value,
                FileFormat.FLAC.value,
                FileFormat.WAV.value,
                FileFormat.MP3.value,
                FileFormat],
            default=FileFormat.DEFAULT.value,
            help="Select format of the recording.",
        )
        parser.add_argument(
            "--sampling-rate", "-r",
            type=int,
            choices=[
                SampleRate.DEFAULT.value,
                SampleRate.R08000.value,
                SampleRate.R16000.value,
                SampleRate.R32000.value,
                SampleRate.R44100.value,
                SampleRate.R48000.value,
                SampleRate.R88200.value,
                SampleRate.R96000.value],
            default=SampleRate.DEFAULT.value,
            help="Select the sampling rate of the recording.",
        )
        parser.add_argument(
            "--bit-depth", "-b",
            type=int,
            choices=[
                Format.S16_LE.get_bit_depth().value,
                Format.S24_3LE.get_bit_depth().value,
                Format.S32_LE.get_bit_depth().value,
            ],
            default=Format.DEFAULT.get_bit_depth().value,
            help="Select the bit depth of the recording.",
        )

        # Audio devices.
        parser.add_argument(
            "--local", "-lcl",
            type=str,
            dest=AudioDevice.LCL.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for local audio device.",
        )
        parser.add_argument(
            "--insert1", "-in1",
            type=str,
            dest=AudioDevice.IN1.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for audio device insert 1.",
        )
        parser.add_argument(
            "--insert2", "-in2",
            type=str,
            dest=AudioDevice.IN2.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for audio device insert 2.",
        )
        parser.add_argument(
            "--external1", "-ex1",
            type=str,
            dest=AudioDevice.EX1.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for external audio device 1.",
        )
        parser.add_argument(
            "--external2", "-ex2",
            type=str,
            dest=AudioDevice.EX2.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for external audio device 2.",
        )

        # Storage devices.
        parser.add_argument(
            "--storage1", "-rc1",
            type=str,
            dest=StorageDevice.RC1.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for storage device 1.",
        )
        parser.add_argument(
            "--storage2", "-rc2",
            type=str,
            dest=StorageDevice.RC2.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for storage device 2.",
        )

        # User interaction.
        parser.add_argument(
            "--input1", "-hi1",
            type=str,
            dest=InputDevice.HI1.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for numeric keyboard.",
        )
        parser.add_argument(
            "--input2", "-hi2",
            type=str,
            dest=InputDevice.HI2.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for Elgato Streamdeck.",
        )
        parser.add_argument(
            "--input3", "-hi3",
            type=str,
            dest=InputDevice.HI3.name,
            default=SKIP_USB_PORT,
            help="Specifies USB port for MorningStar MIDI controller.",
        )
        parser.add_argument(
            "--allowed-storage-usb-ids",
            type=self._validate_hex_string,
            nargs="+",
            # Use name: StorageParameters.allowed_usb_ids
            dest="allowed_usb_ids",
            default=["2d9b"],
            help=("RC Storage vendor id whitelist; e.g. '2d9b' [iStorage], "
                  "'2d9b:8064' [iStorage datAshur Pro2 64GB]."),
        )

        parser.add_argument(
            "-t", "--record-targets",
            type=self._validate_record_targets,
            nargs="*",
            dest="record_targets",
            default=[MixbusDevice.MX0.name],
            help=(
                f"Mixbus devices to record. Valid values: "
                f"{', '.join(e.name for e in MixbusDevice)}."
            ),
        )

        result = parser.parse_args()

        return result
