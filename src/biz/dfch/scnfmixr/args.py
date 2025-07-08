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

"""Module Arguments."""

import argparse
from dataclasses import dataclass
import re

from biz.dfch.i18n import LanguageCode

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
                format: [0-9a-fA-F]{4}.
        Returns:
            str: The unmodified value.

        Raises:
            ArgumentTypeError: If the specified value is not a valid hex
                string.
        """

        if re.fullmatch(r'[0-9A-Fa-f]{4}', value):
            return str

        raise argparse.ArgumentTypeError(
            f"'{value}' is not valid. Format: '[0-9a-fA-F]{{4}}'.")

    def get(self) -> argparse.Namespace:
        """Returns an instance to the argument parser.

        Returns:
            argparse.Namspace: The namespace of the parsed argumentt.
        """

        description = f"""%(prog)s (Secure Conference Mixer and Recorder), v{self.version}

Copyright 2024, 2025 d-fens GmbH. Licensed unter MIT license.
"""  # noqa: E501

        # Process command line arguments.
        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=("For more information see "
                    "https://github.com/dfensgmbh/biz.dfch.PhoneTap/.")
        )

        parser.add_argument(
            "--version", "-v",
            action="version",
            version=f"%(prog)s, v{self.version}"
        )
        parser.add_argument(
            "--service", "-s",
            action="store_true",
            help="Run %(prog)s as service."
        )
        parser.add_argument(
            "--language", "-l",
            type=str,
            choices=[LanguageCode.DEFAULT,
                     LanguageCode.EN.name, LanguageCode.DE.name,
                     LanguageCode.FR.name, LanguageCode.IT.name,
                     ],
            default=LanguageCode.DEFAULT.name,
            help="Select the user interface language."
        )

        # Audio format and audio parameters.
        parser.add_argument(
            "--format", "-f",
            type=str,
            choices=["flac", "wav", "mp3"],
            default="flac",
            help="Select format of the recording."
        )
        parser.add_argument(
            "--sampling-rate", "-r",
            type=int,
            choices=[48000, 8000, 16000, 32000, 44100],
            default=48000,
            help="Select the sampling rate of the recording."
        )
        parser.add_argument(
            "--bit-depth", "-b",
            type=int,
            choices=[24, 16, 32],
            default=24,
            help="Select the bit depth of the recording."
        )
        parser.add_argument(
            "--dual-recording", "-d",
            action="store_true",
            help=("Enable dual recording to storage devices in parallel "
                  "(if connected).")
        )

        # Audio devices.
        parser.add_argument(
            "--local", "-lcl",
            type=str,
            dest="LCL",
            default="1-1",
            help="Specifies USB port for local audio device."
        )
        parser.add_argument(
            "--external1", "-ex1",
            type=str,
            dest="EX1",
            default="1-2",
            help="Specifies USB port for external audio device 1."
        )
        parser.add_argument(
            "--external2", "-ex2",
            type=str,
            dest="EX2",
            default="3-2",
            help="Specifies USB port for external audio device 2."
        )

        # Storage devices.
        parser.add_argument(
            "--storage1", "-rc1",
            type=str,
            dest="RC1",
            default="4-1.3",
            help="Specifies USB port for storage device 1."
        )
        parser.add_argument(
            "--storage2", "-rc2",
            type=str,
            dest="RC2",
            default="4-1.1",
            help="Specifies USB port for storage device 2."
        )

        # User interaction.
        parser.add_argument(
            "--input1", "-hi1",
            type=str,
            dest="HI1",
            default="3-1.4",
            help="Specifies USB port for keyboard."
        )
        parser.add_argument(
            "--input2", "-hi2",
            type=str,
            dest="HI2",
            default="3-1.4",
            help="Specifies USB port for Elgato Streamdeck."
        )
        parser.add_argument(
            "--input3", "-hi3",
            type=str,
            dest="HI3",
            default="3-1.4",
            help="Specifies USB port for MorningStar MIDI controller."
        )
        parser.add_argument(
            "--allowed-storage-vendor-ids",
            type=self._validate_hex_string,
            nargs="+",
            dest="RC_VENDOR_IDS",
            default=["2009"],
            help="RC Storage vendor id whitelist; e.g. 2009: iStorage."
        )

        parser.add_argument(
            "--test", "-t",
            action="store_true",
            help="Test HID detection."
        )
        result = parser.parse_args()

        return result
