[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.PhoneTap&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.PhoneTap)

# biz.dfch.PhoneTap
PhoneTap running on Raspberry Pi OS (Pi 5)

# TOC

- [Installation](#installation)
- [Testing](#testing)
- [Hardware and Software Requirements](#hardware-and-software-requirements)
- [Pi USB Port Layout](#pi-usb-port-layout)
- [Icy Box USB Port Layout](#icy-box-usb-port-layout)
- [License and Copyright](#license-and-copyright)

# Installation

```sh
admin@raspberrypi:~ $ pwd
/home/admin

# Install Python, PIP
sudo apt install python3 python3-pip

# Create virtual environment
cd ~/scnfmixr
python3 -m venv venv
source ~/scnfmixr/venv/bin/activate

# Upgrade PIP
pip install --upgrade pip

# Install packages
pip install argparse
pip install dataclasses
pip install typing

# Save requirements
pip freeze > requirements.txt

# Create script
nano ~/scnfmixr/src/__main__.py

# Make script executable
chmod +x ~/scnfmixr/src/__main__.py

# Create log file and set permissions
sudo touch ~/scnfmixr/app.log
sudo chown admin:root ~/scnfmixr/app.log
sudo chmod 660 ~/scnfmixr/app.log

# Create service descriptor
nano ~/scnfmixr/src/app.service

# Activate and start service
sudo ln -fs ~/scnfmixr/src/app.service /etc/systemd/system/scnfmixr.service
sudo systemctl enable scnfmixr.service
sudo systemctl daemon-reload
sudo systemctl start scnfmixr.service
sudo systemctl status scnfmixr.service
journalctl -u scnfmixr.service
# tail -f app.log

# Deactivate service
sudo systemctl disable scnfmixr.service
sudo systemctl stop scnfmixr.service
sudo systemctl status scnfmixr.service
```

# Testing
```sh
admin@raspberrypi:~ $ pwd
/home/admin
admin@raspberrypi:~ $ cd ~/scnfmixr
admin@raspberrypi:~ $ python -m unittest discover
admin@raspberrypi:~ $ python -m unittest discover -s tests -t . -p test_*.py
admin@raspberrypi:~ $ python -m unittest discover -v -s <package-path> -t . -p test_*.py
# Example: Test single package.
admin@raspberrypi:~ $ python -m unittest discover -v -s tests/my_package -t . -p test_*.py
# Example: Test single module.
admin@raspberrypi:~ $ python -m unittest discover -v -s tests -t . -p test_MyModule.py
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

### Icy Box IB-AC618 USB Port Layout

The USB ports of the Icy Box IB-AC618 have the following numbering (when connected top left, `3-1`, or to bottom left, `1-1`):

| Port  | Type  | USB id  | Path  | Remark  |
|---------|----------|------------|----------------------------------|-------------------------|
| Port 1  | USB 3.0  | `3-1.1`    | `/sys/bus/usb/devices/3-1.1/  `  | as labelled on the hub, connected Top Left  |
| Port 2  | USB 3.0  | `3-1.2`    | `/sys/bus/usb/devices/3-1.2/  `  | as labelled on the hub, connected Top Left  |
| Port 3  | USB 3.0  | `3-1.3`    | `/sys/bus/usb/devices/3-1.3/  `  | as labelled on the hub, connected Top Left  |
| Port 4  | USB 3.0  | `3-1.4.1`  | `/sys/bus/usb/devices/3-1.4.1/`  | as labelled on the hub, connected Top Left  |
| Port 5  | USB 3.0  | `3-1.4.2`  | `/sys/bus/usb/devices/3-1.4.2/`  | as labelled on the hub, connected Top Left  |
| Port 6  | USB 3.0  | `3-1.4.3`  | `/sys/bus/usb/devices/3-1.4.3/`  | as labelled on the hub, connected Top Left  |
| Port 7  | USB 3.0  | `3-1.4.4`  | `/sys/bus/usb/devices/3-1.4.4/`  | as labelled on the hub, PD `5V @2.4A`, connected Top Left  |
|  |  |  |  | |  
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

### Icy Box IB-AC6104-B USB Port Layout

The USB ports of the Icy Box IB-AC618 have the following numbering (when connected top left, `3-1`, or to bottom left, `1-1`):

| Port  | Type  | USB id  | Path  | Remark  |
|---------|----------|------------|------------------------------|-------------------------|
| Port 1  | USB 3.0  | `3-1.1`  | `/sys/bus/usb/devices/3-1.1/`  | 2nd from the cable, connected Top Left  |
| Port 2  | USB 3.0  | `3-1.2`  | `/sys/bus/usb/devices/3-1.2/`  | 3rd from the cable, connected Top Left  |
| Port 3  | USB 3.0  | `3-1.3`  | `/sys/bus/usb/devices/3-1.3/`  | 4th from the cable, connected Top Left  |
| Port 4  | USB 3.0  | `3-1.4`  | `/sys/bus/usb/devices/3-1.4/`  | next to the cable, connected Top Left  |
|  |  |  |  | |  
| Port 1  | USB 3.0  | `1-1.1`  | `/sys/bus/usb/devices/1-1.1/`  | 2nd from the cable, connected Bottom Left  |
| Port 2  | USB 3.0  | `1-1.2`  | `/sys/bus/usb/devices/1-1.2/`  | 3rd from the cable, connected Bottom Left  |
| Port 3  | USB 3.0  | `1-1.3`  | `/sys/bus/usb/devices/1-1.3/`  | 4th from the cable, connected Bottom Left  |
| Port 4  | USB 3.0  | `1-1.4`  | `/sys/bus/usb/devices/1-1.4/`  | next to the cable, connected Bottom Left  |

Note1: If a high speed USB3 device is connected (shown as `5000M` in `lusub -t`), then the bus number will change from **`3`** to **`4`**.
Note2: The hub the following internal port numbering, from left to the right (where the cable is): **3-2-1-4**. So, port 4 is the port directly next to the cable; port 3 is on the opposite end.

# Pin Layout

## TRRS plug to TRS socket "headphones splitter"

This is the typical contact layout for a (OMTP) TRRS adaptetr that splits the TRRS signal into headphones and mic signal.

*tbd*

# Build

The programme should be built with `pyinstaller` as `--onefile`. The resulting executable will be copied into `/opt/...` and started from there. As it is `--onefile` it will be unpacked on start into `/tmp/_MEI...`. By default, logs will be written to the current working directory into `app.log` (truncated on every start); this can be changed in `logging.conf` (obviously before packing into `--onefile`).

```
user@system:~/{project-root} $ pyinstaller --clean --onefile \
    --name scnfmixr \
    --add-data "./src/logging.conf:." \
    --add-data "./src/biz/dfch/scnfmixr/res/:./res/" \
    -p ./src -p ./src/biz \
    ./src/biz/__main__.py;
```

## Source Directory
```
~/project-root
|
- app.log
- logging.conf
+ src
    |
    + biz
        |
        - __init__.py
        - __main__.py           # Use absolute imports here.
        + dfch                  # Relative imports from here.
            |                   # This package is generally empty.
            + scnfmixr          # Actual programme.
                |
                - __init__.py
                - app.py        # Entry point.
                + res           # Contains resources and audio files.
                    |
                    + EN
                        - res.(flac|wav)
                    + DE
                        - res.(flac|wav)
                    + FR
                        - res.(flac|wav)
                    + IT
                        - res.(flac|wav)
+ tests                         # Same structure as 'src' layout, but 
|                               # 'biz' and 'dfch' are omitted.
+ venv      # Windows 11 venv
+ venvdeb   # WSL2 debian venv
+ venvpi    # Pi OS debian venv
+ dist
    |
    - scnfmixr-{arch}-v{maj}.{min}.{rev}
```

## Notes:

pyinstaller parameters

* `-p` on both directories seem to be necessary for successful `import` resolving.
* `--add-data` needed for `logging.conf` and audio files. Or use a separate file for `add-data`.
* On Windows use `;` instead of `:` for `--add-data`.

# Installation and Running the Programme

The programme will create a new `app.log` in the current working directory upon every start.

## Running from source

The programme needs to be run in `src` when running from source: 
`(venv...) user@system:~/{project-root}/src $ python -m biz`

## Running as service

* The programme is intended to run as a `systemd` service..
* The programme depends on JACK to run as a `systemd` service (running as `root`).
* The programme is intended and tested to run on Raspberry Pi 5 under `bookworm-lite`.

```
sudo loginctl enable-linger $USER
sudo usermod -aG audio "$USER"

sudo tee /etc/security/limits.d/audio.conf > /dev/null <<EOF
@audio   -  rtprio     95
@audio   -  memlock    unlimited
EOF

# Packages to be installed:
sudo apt-get -y install pipewire pipewire-alsa pipewire-pulse pipewire-jack wireplumber zita-ajbridge flac sndfile-tools ecasound jackd2 jack-tools exfat-fuse exfatprogs jack-capture lv2-dev lilv-utils x42-plugins zam-plugins calf-plugins lsp-plugins mpd mpc
```

#### Fix missing jack-capture on Debian Trixie

```sh
cd ~  
wget http://deb.debian.org/debian/pool/main/j/jack-capture/jack-capture_0.9.73-3_arm64.deb  
sudo apt -y install ./jack-capture_0.9.73-3_arm64.deb
```

**Ignore this NOTICE:**

```
Notice: Download is performed unsandboxed as root as file '/home/admin/jack-capture_0.9.73-3_arm64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```

### jackd.service

As `admin` create with `nano ~/.config/systemd/user/jackd.service`:

```
[Unit]
Description=JACK audio server (dummy backend)
After=sound.target

[Service]
ExecStart=/usr/bin/jackd -R -ddummy -r48000 -p1024 -C2 -P2
Restart=on-failure

[Install]
WantedBy=default.target
```

### Enabling, starting and stopping the jackd.service

```
systemctl --user daemon-reexec
systemctl --user daemon-reload

$
systemctl --user enable jackd.service
systemctl --user status jackd.service
```

Note: it has been reported, that `status` will not show JACK running, despite it is. Check with `ps aux | grep -i jack` and `jack_lsp` instead.

### scnfmixr.service

As `admin` create with `nano ~/.config/systemd/user/scnfmixr.service`:

```
[Unit]
Description=scnfmixr (Secure Conference Mixer and Recorder)
After=sound.target

[Service]
ExecStart=/opt/scnfmixr/bin/scnfmixr --service
User=root
WorkingDirectory=/opt/scnfmixr
StandardOutput=journal
StandardError=journal
Restart=always

[Install]
WantedBy=default.target
```

### Enabling, starting and stopping the scnfmixr.service

```
# Disable service.
sudo systemctl --user disable scnfmixr.service
sudo systemctl --user stop scnfmixr.service
sudo systemctl --user daemon-reload

# Enable service.
sudo systemctl --user enable scnfmixr.service
sudo systemctl --user daemon-reload
sudo systemctl --user start scnfmixr.service
sudo systemctl --user status scnfmixr.service
journalctl -u scnfmixr.service
```

### mpd@.service

As `admin` create with `nano ~/.config/systemd/user/mpd@.service`:

```
[Unit]
Description=Music Player Daemon (%i)
After=sound.target

[Service]
ExecStart=/usr/bin/mpd --no-daemon %h/.config/mpd/%i/mpd.conf
Restart=on-abort

[Install]
WantedBy=default.target
```

### Enabling, starting and stopping the mpd@.service

Note: The configuration files are defined for user `admin` with `uid` `1000`.

```
# Create links for 
mkdir ~/MpdMusic
mkdir ~/MpdMusic/playback
ln ~/MpdMusic/playback/EN ~/PhoneTap/src/biz/dfch/scnfmixr/res/EN/
ln ~/MpdMusic/playback/DE ~/PhoneTap/src/biz/dfch/scnfmixr/res/DE/
ln ~/MpdMusic/playback/FR ~/PhoneTap/src/biz/dfch/scnfmixr/res/FR/
ln ~/MpdMusic/playback/IT ~/PhoneTap/src/biz/dfch/scnfmixr/res/IT/

mkdir ~/MpdMusic/menu
ln ~/MpdMusic/menu/rc1 ~/mnt/rc1/
ln ~/MpdMusic/menu/rc2 ~/mnt/rc2/
```

```
systemctl --user enable --now mpd@playback.service
systemctl --user enable --now mpd@menu.service
```

#### Testing:

```
systemctl --user status mpd@menu.service
systemctl --user status mpd@playback.service
```

The individual MPD instances communicate via sockets with the (MPC) client:

```
/run/user/1000/mpd.playback.socket
/run/user/1000/mpd.menu.socket
```

The client will use that socket if it is defined in the environment variable `MPD_HOST`. So, we can run the following commands from the shell to communicate with the respective instances:

```
MPD_HOST=/run/user/1000/mpd.menu.socket mpc update
MPD_HOST=/run/user/1000/mpd.menu.socket mpc status

MPD_HOST=/run/user/1000/mpd.playback.socket mpc update
MPD_HOST=/run/user/1000/mpd.playback.socket mpc status
```

Note: as mentioned above, the user id is hardcoded to `1000` (which is `admin`).



## Target Directory
```
/
|
+ home
    |
    + admin
        |
        + .config/systemd/user
            |
            - jackd.service # Service running as admin
+ opt
    |
    + scnfmixr              # Working directory
        |
        - app.log
        - app.service
        + bin
            | 
            - scnfmixr >>> scnfmixr-v{maj}.{min}.{rev}
            - scnfmixr-v{maj}.{min}.{rev}
```

Note: naming for the executable does not have to follow [SemVer](http://semver.org). To allow multiple installed versions the programme directory can be changed from `scnfmixr` to `scnfmixr-v{maj}.{min}.{rev}` and then the executable obviously can be named without version information (which is optional anyway). And there can be only one version of the programme running anyway.

# Detecting the Elgato Streamdeck MK.2

The system works with the Elgato Streamdeck MK.2 device (and only this device). This device has 15 buttons. The button in the upper left corner has id 0 and the button in the lower right corner has id 14.

* [HID API](https://docs.elgato.com/streamdeck/hid/)
* [Stream Deck Module 15 and 32 Keys](https://docs.elgato.com/streamdeck/hid/module-15_32)

The system uses `hexdump` to detect button pushes. `Report` messages start with `0x01 0x00 0x0f 0x00`:

* +00: 0x01 Report ID
* +01: 0x00 Command
* +02: 0x0f (0x00f0) The Streamdeck mkII has 15 keys
* +03: 0x00 
* +04: Payload

The system is only interested in "key press" events, so only the first 4 + 15 bytes are interpreted.

```sh
admin@scnfmixr:~ $ hexdump -C /dev/hidraw1
                                                        #11
                      #0 #1 #2 #3  #4 #5 #6 #7 #8 #9 #10
00000000  01 00 0f 00 01 00 00 00  00 00 00 00 00 00 00 00  |................|
             #13
          #12   #14
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
```

```sh
admin@scnfmixr:~ $ hexdump -C /dev/hidraw1
00000000  01 00 0f 00 01 00 00 00  00 00 00 00 00 00 00 00  |................|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000210  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000400  01 00 0f 00 00 01 00 00  00 00 00 00 00 00 00 00  |................|
00000410  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000600  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000610  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000800  01 00 0f 00 00 00 01 00  00 00 00 00 00 00 00 00  |................|
00000810  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000a00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000a10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000c00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 01 00  |................|
00000c10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000e00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000e10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001000  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 01  |................|
00001010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001200  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001210  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001400  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001410  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001420  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001600  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001610  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001800  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001810  00 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001820  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001a00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001a10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001c00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001c10  00 00 01 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001c20  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001e00  01 00 0f 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001e10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
```

## Detecting the Elgato Streamdeck MK.2

The device has the USB ids that follow:

* vendor id:  0x0fd9
* product id: 0x0080

```sh
admin@scnfmixr:~ $ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 003 Device 002: ID 2e8a:000e Raspberry Pi USB3 HUB
Bus 003 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 002 Device 004: ID 0b0e:0422 GN Netcom Jabra SPEAK 510 USB
Bus 002 Device 007: ID 0fd9:0080 Elgato Systems GmbH Stream Deck MK.2
                       ^^^^ ^^^^
Bus 002 Device 002: ID 2e8a:000d Raspberry Pi USB3 HUB
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

The device will register as a `hidraw` device:

```sh
admin@scnfmixr:~ $ ls -ls /dev/hidraw*
0 crw-rw----+ 1 root plugdev 242, 0 Jan 01 08:15 /dev/hidraw0
0 crw-rw----+ 1 root plugdev 242, 1 Jan 01 08:15 /dev/hidraw1
```

The system queries the vendor id and the product id with `udevadm`. In addition to the vendor id and product id, the USB 2.0 path is known (here `2-1.2`):

```sh
admin@scnfmixr:~ $ udevadm info --no-pager /dev/hidraw1
P: /devices/platform/axi/1000120000.pcie/1f00200000.usb/xhci-hcd.0/usb2/2-1/2-1.2/2-1.2:1.0/0003:0FD9:0080.0005/hidraw/hidraw1

... (output omitted) ...

```

## Layout


|  | **Column 1** | **Column 2** | **Column 3** | **Column 4** | **Column 5** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Row 1** | 0<br />(0x00) | 1<br />(0x01) | 2<br />(0x02) | 3<br />(0x03) | 4<br />(0x04) |
| **Row 2** | 5<br />(0x05) | 6<br />(0x06) | 7<br />(0x07) | 8<br />(0x08) | 9<br />(0x09) |
| **Row 3** | 10<br />(0x0A) | 11<br />(0x0B) | 12<br />(0x0C) | 13<br />(0x0D) | 14<br />(0x0E) |

![Keypad Keys Index Layout](https://docs.elgato.com/img/streamdeck/hid/sd-classic-buttons-layout.png)

NOTE: See [Stream Deck Module 15 and 32 Keys](https://docs.elgato.com/streamdeck/hid/module-15_32) for further information.

## Installing Python libraries

The system uses the [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck) library from [abcminiuser](https://github.com/abcminiuser) (licensed under the [MIT license](https://github.com/abcminiuser/python-elgato-streamdeck/blob/master/LICENSE)).

We need to install:

* libhidapi-libusb0
  ```sh
  sudo apt-get install libhidapi-libusb0
  ```

* Streamdeck
  ```sh
  pip install Streamdeck
  ```

* Pillow>=9.0.0
  ```sh
  # Pillow>=9.0.0
  pip install -r requirements.txt
  ```

# Notes and Observations

* Normally, when connecting a device to the "Icy Box IB-AC618", a blue LED turns on next to the connected device. However, when connecting a *UGREEN* USB audio adapter it only shows when there is a 3.5mm TRRS cable connected to its socket. (`12d1:0010 Huawei Technologies Co., Ltd. KT USB Audio`). The same happens with the *Atomos Connect 4K* when there is no HDMI cable connected.
* Also for "Icy Box IB-AC618": The Speakerphone (or any device with a rechargeable battery) should be connected to port 7 on the USB hub as that port can provide the most power.

# License and Copyright

Everything in this repository (unless otherwise noted) is licensed under the GPLv3 (see [LICENSE](./LICENSE)) and is copyright of: 

**[d-fens GmbH](https://zefix.ch/en/search/entity/list/firm/989185)**

**General-Guisan-Strasse 6**

**CH-6300 Zug**

**SCHWEIZ**

## Licenses of third-party components

See [NOTICE](NOTICE.md) for license of third-party components.
