# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH

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
import logging
import os
import re
import subprocess
import sys
import time


@dataclass(frozen=True)
class UsbDeviceInfo:
    idVendor: str
    idProduct: str
    serial: str


@dataclass(frozen=True)
class AsoundCardInfo:
    usbDeviceInfo: UsbDeviceInfo
    idCard: int


def read_first_line(file_path: str) -> str:
    """Reads the first text line of the specified file and returns it. File is opend ReadOnly. No error checking is performed.

    Args:
        file_path (str): file to read from in ReadOnly mode.

    Returns:
        str: the first line read from the specified file.
    """
    with open(file_path, 'r') as file:
        return file.readline().strip()


def get_usbid(usb_bus_number: str) -> str:
    sys_bus_usb_devices_basepath = '/sys/bus/usb/devices/'
    sys_bus_usb_device_path = f'{sys_bus_usb_devices_basepath}{usb_bus_number}'
    idVendor = read_first_line(f'{sys_bus_usb_device_path}/idVendor')
    idProduct = read_first_line(f'{sys_bus_usb_device_path}/idProduct')
    return f'{idVendor}:{idProduct}'


def get_usb_device_info(usb_bus_number: str) -> UsbDeviceInfo:
    sys_bus_usb_devices_basepath = '/sys/bus/usb/devices/'
    # sys_bus_usb_device_path = f'{sys_bus_usb_devices_basepath.rstrip(os.sep)}{os.sep}{usb_bus_number}'
    sys_bus_usb_device_path = os.path.join(sys_bus_usb_devices_basepath, usb_bus_number)
    # idVendor = read_first_line(f'{sys_bus_usb_device_path.rstrip(os.sep)}{os.sep}idVendor')
    idVendor = read_first_line(os.path.join(sys_bus_usb_device_path, 'idVendor'))
    # idProduct = read_first_line(f'{sys_bus_usb_device_path.rstrip(os.sep)}{os.sep}idProduct')
    idProduct = read_first_line(os.path.join(sys_bus_usb_device_path, 'idProduct'))
    # serial = read_first_line(f'{sys_bus_usb_device_path.rstrip(os.sep)}{os.sep}serial')
    serial = read_first_line(os.path.join(sys_bus_usb_device_path, 'serial'))
    return UsbDeviceInfo(idVendor=idVendor, idProduct=idProduct, serial=serial)


def get_asound_info(usbDeviceInfo: UsbDeviceInfo) -> AsoundCardInfo:
    proc_asound_basepath = '/proc/asound/'
    pattern = r'^card(\d+)$'
    target_usbid = f'{usbDeviceInfo.idVendor}:{usbDeviceInfo.idProduct}'
    for dir_name in os.listdir(proc_asound_basepath):
        try:
            match = re.match(pattern, dir_name)
            if not match:
                continue
            card_path = os.path.join(proc_asound_basepath, dir_name)
            print(card_path)
            card_usbid_file = f'{card_path.rstrip(os.sep)}{os.sep}usbid'
            usbid = read_first_line(card_usbid_file)
            if usbid.lower() == target_usbid.lower():
                return AsoundCardInfo(usbDeviceInfo=usbDeviceInfo, idCard=match.group(1))
        except Exception:
            continue


def run_loop():
    try:
        device_info = get_usb_device_info('1-1.3')
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


logging.basicConfig(
    filename='/home/admin/PhoneTap20/main.log',
    level=logging.INFO,
    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s'
)


def startup_loop():
    print(f"Running script as startup ... '{time.localtime().tm_sec}'")
    logging.info("Running script as startup ...")
    run_loop()

    if 5 == time.localtime().tm_sec:
        try:
            ASOUND_CARDS = '/proc/asound/cards'
            # result = subprocess.run(['cat', ASOUND_CARDS], capture_output=True, text=True, check=True)
            # contents = result.stdout
            with open(ASOUND_CARDS, 'r') as file:
                contents = file.read()
            for line in contents.splitlines():
                print(line)
                logging.info(line)
            raise Exception("Current second is 5. Raising an exception ...")

        except subprocess.CalledProcessError:
            raise

    return


def startup():
    while True:
        try:
            startup_loop()
            time.sleep(1)
        except Exception as e:
            logging.info(f"startup() FAILED with exception '{e}'. Restarting ...")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="PhoneTap20 Main Script")
    parser.add_argument(
        '--startup', '-s',
        action='store_true',
        help='PhoneTap20 startup loop'
    )
    args = parser.parse_args()

    if args.startup:
        startup()
        #print("Running script as part of startup ...")
        #logging.info("Running script as part of startup ...")
        # Add your startup logic here

        sys.exit(8)
    else:
        print("Running script normally ...")
        logging.info("Running script normally ...")
        # Add normal script logic here

        sys.exit(9)


if __name__ == "__main__":
    main()
