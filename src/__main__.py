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

import argparse
import subprocess
import sys
import time

from env_embedded import Asound, Usb
from jack_commands import JackConnection, ZitaBridgeAlsaToJack, ZitaBridgeJackToAlsa
from log import log
from Version import Version


def run_loop():
    try:
        # Detect Jabra SPEAK 510
        device_info_lcl = Usb.get_usb_device_info("1-1")
        asound_info_lcl = Asound.get_info(device_info_lcl)
        wav_file = "/home/admin/PhoneTap20/src/snd/CardA.Connected.EN.wav"
        params = ["aplay", "-D", f"plughw:{asound_info_lcl.idCard}", wav_file]
        _ = subprocess.run(params)

        try:
            # Detect Sound Devices MixPre-3 II
            device_info_rec = Usb.get_usb_device_info("3-1")
            asound_info_ex1 = Asound.get_info(device_info_rec)
            wav_file = "/home/admin/PhoneTap20/src/snd/CardA.Connected.DE.wav"
            params = ["aplay", "-D", f"plughw:{asound_info_ex1.idCard}", wav_file]
            _ = subprocess.run(params)

            try:
                # JABRA
                _ = ZitaBridgeAlsaToJack("LCL-I", f"hw:{asound_info_lcl.idCard},0", 1, 16000)
                _ = ZitaBridgeJackToAlsa("LCL-O", f"hw:{asound_info_lcl.idCard},0", 2, 48000)

                # MixPre-3
                _ = ZitaBridgeAlsaToJack("EX1-I", f"hw:{asound_info_ex1.idCard},0", 2, 48000)
                _ = ZitaBridgeJackToAlsa("EX1-O", f"hw:{asound_info_ex1.idCard},0", 2, 48000)

                time.sleep(10)

                _ = JackConnection.Factory.create("LCL-I:capture_1", "EX1-O:playback_1")
                _ = JackConnection.Factory.create("LCL-I:capture_1", "EX1-O:playback_2")

                _ = JackConnection.Factory.create("EX1-I:capture_1", "LCL-O:playback_1")
                _ = JackConnection.Factory.create("EX1-I:capture_2", "LCL-O:playback_2")

                time.sleep(60)

            except Exception:
                time.sleep(1)

        except Exception:
            time.sleep(1)

        time.sleep(5)

    except Exception:
        # wav_file = '/home/admin/PhoneTap20/src/snd/CardA.Disconnected.EN.wav'
        # params = ['aplay', '-D', f'plughw:{asound_info.idCard}', wav_file]
        # result = subprocess.run(params)
        time.sleep(1)


def arg_startup():
    while True:
        try:
            log.info(f"Running script as startup ... '{time.localtime().tm_sec}'")
            run_loop()
            time.sleep(1)
        except Exception as e:
            log.info(f"startup() FAILED with exception '{e}'. Restarting ...")
            time.sleep(5)


def main():
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
