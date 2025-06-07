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
                # /usr/bin/jackd -ddummy -r48000 -p1024
                params = ["/usr/bin/jackd", "-ddummy", "-r48000", "-p1024"]
                log.info(params)
                _ = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # _ = subprocess.run(params)
                time.sleep(10)

                # Jabra
                params = [
                    "/usr/bin/zita-a2j",
                    "-j",
                    "LCL_IN",
                    "-d",
                    f"hw:{asound_info_lcl.idCard},0",
                    "-c",
                    "1",
                    "-r",
                    "16000",
                ]
                log.info(params)
                _ = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                params = [
                    "/usr/bin/zita-j2a",
                    "-j",
                    "LCL_OUT",
                    "-d",
                    f"hw:{asound_info_lcl.idCard},0",
                    "-c",
                    "2",
                    "-r",
                    "48000",
                ]
                log.info(params)
                _ = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # MixPre-3
                params = [
                    "/usr/bin/zita-a2j",
                    "-j",
                    "REC_IN",
                    "-d",
                    f"hw:{asound_info_ex1.idCard},0",
                    "-c",
                    "2",
                    "-r",
                    "48000",
                ]
                log.info(params)
                _ = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                params = [
                    "/usr/bin/zita-j2a",
                    "-j",
                    "REC_OUT",
                    "-d",
                    f"hw:{asound_info_ex1.idCard},0",
                    "-c",
                    "2",
                    "-r",
                    "48000",
                ]
                log.info(params)
                _ = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                time.sleep(10)

                params = ["/usr/bin/jack_connect", "LCL_IN:capture_1", "REC_OUT:playback_1"]
                log.info(params)
                _ = subprocess.run(params)
                params = ["/usr/bin/jack_connect", "LCL_IN:capture_1", "REC_OUT:playback_2"]
                log.info(params)
                _ = subprocess.run(params)

                params = ["/usr/bin/jack_connect", "REC_IN:capture_1", "LCL_OUT:playback_1"]
                log.info(params)
                _ = subprocess.run(params)
                params = ["/usr/bin/jack_connect", "REC_IN:capture_2", "LCL_OUT:playback_2"]
                log.info(params)
                _ = subprocess.run(params)

                time.sleep(60)

            except Exception:
                log.error("Could not start jackd")
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
