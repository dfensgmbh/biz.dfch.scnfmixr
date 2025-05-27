# biz.dfch.PhoneTap
PhoneTap running on Raspberry Pi OS (Pi 5)

# Installation

```sh

admin@raspberrypi:~ $ pwd
/home/admin

# Install Python, PIP
sudo apt install python3 python3-pip

# Create virtual environment
cd ~/PhoneTap20
python3 -m venv venv
source ~/PhoneTap20/venv/bin/activate

# Upgrade PIP
pip install --upgrade pip

# Install packages
pip install argparse
pip install dataclasses
pip install typing

# Save requirements
pip freeze > requirements.txt

# Create script
nano ~/PhoneTap20/src/main.py

# Make script executable
chmod +x ~/PhoneTap20/src/main.py

# Create log file and set permissions
sudo touch ~/PhoneTap20/main.log
sudo chown admin:root ~/PhoneTap20/main.log
sudo chmod 660 ~/PhoneTap20/main.log

# Create service descriptor
nano ~/PhoneTap20/src/main.service

# Activate and start service
sudo ln -s ~/PhoneTap20/src/main.service /etc/systemd/system/PhoneTap20.service
sudo systemctl enable PhoneTap20.service
sudo systemctl daemon-reload
sudo systemctl start PhoneTap20.service
sudo systemctl status PhoneTap20.service

# Deactivate service
sudo systemctl disable PhoneTap20.service
sudo systemctl stop PhoneTap20.service
sudo systemctl status PhoneTap20.service
```

# Testing
```sh
admin@raspberrypi:~ $ pwd
/home/admin
admin@raspberrypi:~ $ cd ~/PhoneTap20
admin@raspberrypi:~ $ python -m unittest discover
```

# Hardware and Software Requirements

The programme is intended to run on a Raspberry Pi 5 with a Raspberry Pi OS '[Bookworm](https://www.raspberrypi.com/news/bookworm-the-new-version-of-raspberry-pi-os/)'. It is tested under the following version:

`Linux raspberrypi 6.12.25+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-04-30) aarch64 GNU/Linux`

## Packages

The following packages are needed:
```
sudo apt-get -y full-upgrade
sudo apt-get -y autoremove
sudo reboot
sudo apt-get -y install pipewire pipewire-alsa pipewire-pulse pipewire-jack qjackctl wireplumber zita-ajbridge
sudo reboot
```

## Hardware

* The OS is running on a [Raspberry Pi 5 8GB](https://www.raspberrypi.com/products/raspberry-pi-5/?variant=raspberry-pi-5-8gb) with its original power supply.
* The board is mounted in a aluminium case with passive cooling, such as [Ridged Armour Case for Raspberry Pi 5](https://thepihut.com/products/ridged-armour-case-for-raspberry-pi-5).
* Additional USB ports are made available via an [ICY BOX IB-AC618 7-port USB 3.0 powered USB adapter (gen1)](https://icybox.de/product/hubs/IB-AC618) (USB-A to USB-B, power supply `12V @3A`).

### Pi USB Port Layout

The internal USB ports of the Pi 5 have the following numbering:

| Port  | Type  | USB id  | Path  | Remark  |
|---------------|----------|--------|--------------------------------|---------------------------------|
| Top Left      | USB 3.0  | `3-1`  | `/sys/bus/usb/devices/3-1/  `  | right next to the RJ45 port     |
| Bottom Left   | USB 3.0  | `1-1`  | `/sys/bus/usb/devices/1-1/  `  | right next to the RJ45 port     |
| Top Right     | USB 2.0  | `1-2`  | `/sys/bus/usb/devices/1-2/  `  | to the right of "Top left"      |
| Bottom Right  | USB 2.0  | `3-2`  | `/sys/bus/usb/devices/3-2/  `  | to the right of "Bottom left"   |

Note: the USB identification shown via `/proc/asound/cards` do not match the `device` numbering, eg. a device connected to `/sys/bus/usb/devices/1-2/` shows up as `usb-xhci-hcd.0-2`. Further note, that the `device` (`Dev`) numbering changes and increments with disconnects and connects even on the same phyiscal port (eg. in the output below the connected device is shown as `Dev 30` but was previously before reconnect shown as `Dev 29`). This number corresponds to `devnum` under `/sys/bus/usb/devices/<usbid>/devnum`. In ALSA this is reflected in ` /proc/asound/card<id>/usbbus` (last part of `001/030`).

```
$ lsusb -t
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
    |__ Port 2: Dev 30, If 0, Class=Audio, Driver=snd-usb-audio, 12M
    |__ Port 2: Dev 30, If 1, Class=Audio, Driver=snd-usb-audio, 12M
    |__ Port 2: Dev 30, If 2, Class=Audio, Driver=snd-usb-audio, 12M
    |__ Port 2: Dev 30, If 3, Class=Human Interface Device, Driver=usbhid, 12M

$ cat /proc/asound/cards
 0 [vc4hdmi0       ]: vc4-hdmi - vc4-hdmi-0
                      vc4-hdmi-0
 1 [vc4hdmi1       ]: vc4-hdmi - vc4-hdmi-1
                      vc4-hdmi-1
 2 [Audio          ]: USB-Audio - KT USB Audio
                      KTMicro KT USB Audio at usb-xhci-hcd.0-2, full speed
```

### Icy Box USB Port Layout

The USB ports of the Icy Box IB-AC618 have the following numbering (when connected top left, `3-1` or to `1-1`):

| Port  | Type  | USB id  | Path  | Remark  |
|---------|----------|------------|----------------------------------|-------------------------|
| Port 1  | USB 3.0  | `3-1.1`    | `/sys/bus/usb/devices/3-1.1/  `  | as labelled on the hub, connected Top Left  |
| Port 2  | USB 3.0  | `3-1.2`    | `/sys/bus/usb/devices/3-1.2/  `  | as labelled on the hub, connected Top Left  |
| Port 3  | USB 3.0  | `3-1.3`    | `/sys/bus/usb/devices/3-1.3/  `  | as labelled on the hub, connected Top Left  |
| Port 4  | USB 3.0  | `3-1.4.1`  | `/sys/bus/usb/devices/3-1.4.1/`  | as labelled on the hub, connected Top Left  |
| Port 5  | USB 3.0  | `3-1.4.2`  | `/sys/bus/usb/devices/3-1.4.2/`  | as labelled on the hub, connected Top Left  |
| Port 6  | USB 3.0  | `3-1.4.3`  | `/sys/bus/usb/devices/3-1.4.3/`  | as labelled on the hub, connected Top Left  |
| Port 7  | USB 3.0  | `3-1.4.4`  | `/sys/bus/usb/devices/3-1.4.4/`  | as labelled on the hub, PD `5V @2.4A`, connected Top Left  |
| Port 1  | USB 3.0  | `1-1.1`    | `/sys/bus/usb/devices/1-1.1/  `  | as labelled on the hub, connected Bottom Left  |
| Port 2  | USB 3.0  | `1-1.2`    | `/sys/bus/usb/devices/1-1.2/  `  | as labelled on the hub, connected Bottom Left  |
| Port 3  | USB 3.0  | `1-1.3`    | `/sys/bus/usb/devices/1-1.3/  `  | as labelled on the hub, connected Bottom Left  |
| Port 4  | USB 3.0  | `1-1.4.1`  | `/sys/bus/usb/devices/1-1.4.1/`  | as labelled on the hub, connected Bottom Left  |
| Port 5  | USB 3.0  | `1-1.4.2`  | `/sys/bus/usb/devices/1-1.4.2/`  | as labelled on the hub, connected Bottom Left  |
| Port 6  | USB 3.0  | `1-1.4.3`  | `/sys/bus/usb/devices/1-1.4.3/`  | as labelled on the hub, connected Bottom Left  |
| Port 7  | USB 3.0  | `1-1.4.4`  | `/sys/bus/usb/devices/1-1.4.4/`  | as labelled on the hub, PD `5V @2.4A`, connected Bottom Left  |

#### USB Tree Layout Top Left, 3-1
```
$ lsusb -t
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
    |__ Port 1: Dev 4, If 0, Class=Hub, Driver=hub/4p, 5000M
        |__ Port 4: Dev 5, If 0, Class=Hub, Driver=hub/4p, 5000M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
    |__ Port 1: Dev 26, If 0, Class=Hub, Driver=hub/4p, 480M
        |__ Port 4: Dev 27, If 0, Class=Hub, Driver=hub/4p, 480M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
```

#### USB Tree Layout Bottom Left, 1-1
```
$ lsusb -t
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/4p, 5000M
        |__ Port 4: Dev 3, If 0, Class=Hub, Driver=hub/4p, 5000M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/2p, 480M
    |__ Port 1: Dev 31, If 0, Class=Hub, Driver=hub/4p, 480M
        |__ Port 4: Dev 32, If 0, Class=Hub, Driver=hub/4p, 480M
```

# License and Copyright
Everything in this repository (unless otherwise noted) is licensed under the MIT license (see [LICENSE](./LICENSE)) and copyright of 

**[d-fens GmbH](https://zefix.ch/en/search/entity/list/firm/989185)**

**General-Guisan-Strasse 6**

**CH-6300 Zug**

**SCHWEIZ**
