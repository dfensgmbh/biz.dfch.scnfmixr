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

"""The entry module to the programme."""

import argparse
import sys
import time

from alsa_usb import AlsaStreamInfoParser
from jack_commands import JackConnection, ZitaBridgeAlsaToJack, ZitaBridgeJackToAlsa
from log import log
from service import SetupDevice
from Version import Version


def run_loop():
    """Main run loop of programme."""

    # Detect local speaker phone
    usb_id = "1-1"
    log.info("LCL: Detecting local speakerphone [%s] ...", usb_id)
    device_lcl = SetupDevice.Factory.create(usb_id)

    # Detect external phone EX1
    usb_id = "1-2"
    log.info("EX1: Detecting external device 1 [%s] ...", usb_id)
    device_ex1 = SetupDevice.Factory.create(usb_id)

    # Detect external recorder
    usb_id = "3-2"
    log.info("REC: Detecting recorder [%s] ...", usb_id)
    device_rec = SetupDevice.Factory.create(usb_id)

    while True:
        try:

            # LCL
            log.info("LCL: Creating JACK clients for '%s' ...", device_lcl.asound_info.idCard)

            parser_lcl = AlsaStreamInfoParser(device_lcl.asound_info.idCard)

            lcl_capture = parser_lcl.get_best_capture_interface()
            log.info("%s: %s", device_lcl.asound_info.idCard, lcl_capture.to_dict())

            lcl_playback = parser_lcl.get_best_playback_interface()
            log.info("%s: %s", device_lcl.asound_info.idCard, lcl_playback.to_dict())

            _ = ZitaBridgeAlsaToJack(
                "LCL-I",
                f"hw:{device_lcl.asound_info.idCard},0",
                lcl_capture.channel_count,
                parser_lcl.best_rate(lcl_capture.rates),
            )
            _ = ZitaBridgeJackToAlsa(
                "LCL-O",
                f"hw:{device_lcl.asound_info.idCard},0",
                lcl_playback.channel_count,
                parser_lcl.best_rate(lcl_playback.rates),
            )

            # EX1
            log.info("EX1: Creating JACK clients for '%s' ...", device_ex1.asound_info.idCard)

            parser_ex1 = AlsaStreamInfoParser(device_ex1.asound_info.idCard)

            ex1_capture = parser_ex1.get_best_capture_interface()
            log.info("%s: %s", device_ex1.asound_info.idCard, ex1_capture.to_dict())

            ex1_playback = parser_ex1.get_best_playback_interface()
            log.info("%s: %s", device_ex1.asound_info.idCard, ex1_playback.to_dict())

            _ = ZitaBridgeAlsaToJack(
                "EX1-I",
                f"hw:{device_ex1.asound_info.idCard},0",
                ex1_capture.channel_count,
                parser_ex1.best_rate(ex1_capture.rates),
            )
            _ = ZitaBridgeJackToAlsa(
                "EX1-O",
                f"hw:{device_ex1.asound_info.idCard},0",
                ex1_playback.channel_count,
                parser_ex1.best_rate(ex1_playback.rates),
            )

            # REC
            log.info("REC: Creating JACK clients for '%s' ...", device_rec.asound_info.idCard)

            parser_rec = AlsaStreamInfoParser(device_rec.asound_info.idCard)

            rec_capture = parser_rec.get_best_capture_interface()
            log.info("%s: %s", device_rec.asound_info.idCard, rec_capture.to_dict())

            rec_playback = parser_rec.get_best_playback_interface()
            log.info("%s: %s", device_rec.asound_info.idCard, rec_playback.to_dict())

            _ = ZitaBridgeAlsaToJack(
                "REC-I",
                f"hw:{device_rec.asound_info.idCard},0",
                rec_capture.channel_count,
                parser_rec.best_rate(rec_capture.rates),
            )
            _ = ZitaBridgeJackToAlsa(
                "REC-O",
                f"hw:{device_rec.asound_info.idCard},0",
                rec_playback.channel_count,
                parser_rec.best_rate(rec_playback.rates),
            )

            # DFTODO - fix timing and then remove this
            time.sleep(3)

            log.info("Creating JACK connections for '%s' ...", device_lcl.asound_info.idCard)
            _ = JackConnection.Factory.create("LCL-I:capture_1", "EX1-O:playback_1")
            _ = JackConnection.Factory.create("LCL-I:capture_1", "EX1-O:playback_2")
            _ = JackConnection.Factory.create("LCL-I:capture_1", "REC-O:playback_1")
            _ = JackConnection.Factory.create("LCL-I:capture_1", "REC-O:playback_2")

            log.info("Creating JACK connections for '%s' ...", device_ex1.asound_info.idCard)
            _ = JackConnection.Factory.create("EX1-I:capture_1", "LCL-O:playback_1")
            _ = JackConnection.Factory.create("EX1-I:capture_1", "LCL-O:playback_2")
            _ = JackConnection.Factory.create("EX1-I:capture_1", "REC-O:playback_1")
            _ = JackConnection.Factory.create("EX1-I:capture_1", "REC-O:playback_2")

            while True:
                log.debug("Keep alive ...")
                time.sleep(5)

        except Exception:  # pylint: disable=broad-exception-caught
            time.sleep(1)


def arg_startup():
    """This function handles argument 'startup'."""
    while True:
        try:
            log.info("Running script as startup ... '%s'", time.localtime().tm_sec)
            run_loop()
            time.sleep(1)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            log.info("startup() FAILED with exception '%s'. Restarting ...", ex)
            time.sleep(5)


def main():
    """The entry point to the programme."""
    Version().ensure_minimum_version(3, 10)

    log.info("Application started. Parsing command-line arguments ...")
    parser = argparse.ArgumentParser(description="PhoneTap20 Main Script")
    parser.add_argument("--startup", "-s", action="store_true", help="PhoneTap20 startup loop")
    args = parser.parse_args()

    if args.startup:
        arg_startup()
        sys.exit(0)

    log.info("Use '-h' or '--help' to see the help text.")
    sys.exit(1)


if __name__ == "__main__":
    main()
