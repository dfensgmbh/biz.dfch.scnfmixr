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
from dataclasses import dataclass
import os
import re
import subprocess
import sys
import time

from src.log import log
from src.TextUtils import TextUtils
from src.Version import Version


@dataclass(frozen=True)
class UsbDeviceInfo:
    idVendor: str
    idProduct: str
    serial: str
    devnum: int


@dataclass(frozen=True)
class AsoundCardInfo:
    usbDeviceInfo: UsbDeviceInfo
    idCard: int


def get_usbid(usbbus_id: str) -> str:

    SYS_BUS_USB_DEVICES_BASEPATH = '/sys/bus/usb/devices/'

    sys_bus_usb_device_path = os.path.join(SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)
    idVendor = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'idVendor'))
    idProduct = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'idProduct'))
    return f'{idVendor}:{idProduct}'


def get_usb_device_info(usbbus_id: str) -> UsbDeviceInfo:

    SYS_BUS_USB_DEVICES_BASEPATH = '/sys/bus/usb/devices/'

    sys_bus_usb_device_path = os.path.join(SYS_BUS_USB_DEVICES_BASEPATH, usbbus_id)

    idVendor = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'idVendor'))
    idProduct = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'idProduct'))
    serial = TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'serial'))
    devnum = int(TextUtils().read_first_line(os.path.join(sys_bus_usb_device_path, 'devnum')))

    return UsbDeviceInfo(idVendor=idVendor, idProduct=idProduct, serial=serial, devnum=devnum)


def get_asound_info(usbDeviceInfo: UsbDeviceInfo) -> AsoundCardInfo | None:

    PROC_ASOUND_BASEPATH = '/proc/asound/'
    CARD_PATTERN = r'^card(\d+)$'
    USBBUS_PATTERN = r'^(\d+)/(\d+)$'

    target_usbid = f'{usbDeviceInfo.idVendor}:{usbDeviceInfo.idProduct}'

    for card_dir_basename in os.listdir(PROC_ASOUND_BASEPATH):
        try:
            match = re.match(CARD_PATTERN, card_dir_basename)
            if not match:
                continue

            card_id = int(match.group(1))
            card_dir_fullpath = os.path.join(PROC_ASOUND_BASEPATH, card_dir_basename)

            # Test if specified usbid matches current card.
            usbid = TextUtils().read_first_line(os.path.join(card_dir_fullpath, 'usbid'))
            if usbid.lower() != target_usbid.lower():
                continue

            # Test if specified devnum matches current card.
            usbbus = TextUtils().read_first_line(os.path.join(card_dir_fullpath, 'usbbus'))
            match = re.match(USBBUS_PATTERN, usbbus)
            if not match:
                continue
            devnum = int(match.group(2))
            if (devnum != usbDeviceInfo.devnum):
                continue

            log.info(f"Card '{card_id}' found for '{target_usbid}' ['{devnum}']")
            return AsoundCardInfo(usbDeviceInfo=usbDeviceInfo, idCard=card_id)

        except Exception:
            continue

    log.warning(f"Card id not found for '{target_usbid}' ['{devnum}']")
    return None


def run_loop():
    try:
        device_info = get_usb_device_info('1-1.4.4')
        asound_info = get_asound_info(device_info)
        wav_file = '/home/admin/PhoneTap20/src/snd/CardA.Connected.EN.wav'
        params = ['aplay', '-D', f'plughw:{asound_info.idCard}', wav_file]
        _ = subprocess.run(params)
        time.sleep(5)

    except Exception:
        # wav_file = '/home/admin/PhoneTap20/src/snd/CardA.Disconnected.EN.wav'
        # params = ['aplay', '-D', f'plughw:{asound_info.idCard}', wav_file]
        # result = subprocess.run(params)
        time.sleep(1)
        pass


# logging.basicConfig(
#     filename='/home/admin/PhoneTap20/main.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(process)d - %(levelname)s - %(module)s - %(message)s'
# )


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
    parser.add_argument(
        '--startup', '-s',
        action='store_true',
        help='PhoneTap20 startup loop'
    )
    args = parser.parse_args()

    if args.startup:
        arg_startup()
        sys.exit(0)

    log.info("Nothing to do. Exiting ...")
    sys.exit(1)


if __name__ == "__main__":
    main()
