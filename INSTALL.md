# Installation on a Compute Module 5 CM5008032

This document gives instructions for the installation of the scnfmixr and its software.

## Installation of the operating system

1. Connect pin 1 and pin 2 of Jumper 2 (J2) (,,Fit Jumper to disable eMMC boot'').
1. Start "rpiboot-CM4-CM5 - Mass Storage Gadget" (RPIBOOT).
1. Connect the USB-C-to-USB-C cable to Jumper 11 (J11) and to the USB-C port of your computer.
1. After some seconds, you see a "mmcblk0p" ("mass storage device" of the Compute Module).
1. Start "Raspberry Pi Imager v1.9.6" (RPIIMAGER).
1. Select "Raspberry Pi 5".
1. Select [`Raspberry Pi OS (64-bit) Lite`](https://downloads.raspberrypi.com/raspios_full_arm64/images/raspios_full_arm64-2025-12-04/2025-12-04-raspios-trixie-arm64-full.img.xz) (the operating system)

   NOTE: If you do see this operating system in the list, select the operating through "Custom image".

1. Select the "mass storage device".
1. Select "Use customization" with these items:

   1. Timezone: ZH
   1. Keyboard layout: ch-de
   1. Username: admin
   1. Create a password.

1. Install the operating system.
1. Wait, until the operating is complete.
1. Disconnect the USB-C-to-USB-C cable from Jumper 11 (J11).
1. Disconnect pin 1 and pin 2 of Jumper 2 (J2).
1. Start the Compute Module 5.

## Login to the Compute Module 5

1.  Make sure, that you can login to the Compute Module 5 with the username `admin`.

## Update the operating system

1.  Make sure, that you are logged in with username `admin`.
1.  Install operating system updates.

```
sudo apt-get -y update
sudo apt-get -y full-upgrade
sudo apt-get -y autoremove
sudo reboot
```

## Installation of system parameters

1.  Make sure, that you are logged in with username `admin`.
1. Do these modifications.

```
sudo loginctl enable-linger $USER
sudo usermod -aG audio "$USER"

sudo tee /etc/security/limits.d/audio.conf > /dev/null <<EOF
@audio   -  rtprio     95
@audio   -  memlock    unlimited
EOF
```

## Installation of necessary packages

1.  Make sure, that you are logged in with username `admin`.
1.  Install the packages that follow.

```
sudo apt-get -y install <packages> # For details, see below.
sudo reboot
```

```sh
# PipeWire - modern audio/video server
sudo apt-get -y install pipewire

# PipeWire ALSA plugin for routing ALSA apps through PipeWire
sudo apt-get -y install pipewire-alsa

# PipeWire PulseAudio replacement/compatibility layer
sudo apt-get -y install pipewire-pulse

# PipeWire JACK compatibility layer
sudo apt-get -y install pipewire-jack

# QjackCtl - graphical JACK connection manager and patch bay
sudo apt-get -y install qjackctl

# WirePlumber - session/policy manager for PipeWire
sudo apt-get -y install wireplumber

# JACK Audio Connection Kit v2 - low-latency audio server
sudo apt-get -y install jackd2

# zita-ajbridge - ALSA to JACK bridge utility
sudo apt-get -y install zita-ajbridge

# Python 3 interpreter
sudo apt-get -y install python3

# pip - Python package installer
sudo apt-get -y install python3-pip

# FLAC - Free Lossless Audio Codec encoder/decoder
sudo apt-get -y install flac

# sndfile-tools - command-line tools for libsndfile (audio file conversion)
sudo apt-get -y install sndfile-tools

# ecasound - multitrack audio processing and recording
sudo apt-get -y install ecasound

# exfat-fuse - FUSE driver for exFAT filesystems
sudo apt-get -y install exfat-fuse

# exfatprogs - exFAT filesystem utilities (mkfs, fsck)
sudo apt-get -y install exfatprogs

# Install ccze colorizer
sudo apt-get -y install ccze

# evtest - tool to monitor and debug Linux input events
sudo apt-get -y install evtest

# MPD - Music Player Daemon (headless music player)
sudo apt-get -y install mpd

# mpc - command-line client for MPD
sudo apt-get -y install mpc

# libhidapi-libusb0 - HID API library using libusb backend
sudo apt-get -y install libhidapi-libusb0

# lv2-dev - LV2 plugin development headers and files
sudo apt-get -y install lv2-dev

# lilv-utils - command-line tools for inspecting LV2 plugins
sudo apt-get -y install lilv-utils

# x42-plugins - collection of LV2 plugins by Robin Gareus
sudo apt-get -y install x42-plugins

# zam-plugins - collection of LV2 audio plugins by ZamAudio
sudo apt-get -y install zam-plugins

# calf-plugins - Calf Studio Gear LV2/LADSPA audio plugins
sudo apt-get -y install calf-plugins

# lsp-plugins - Linux Studio Plugins (LV2/LADSPA/VST audio effects)
sudo apt-get -y install lsp-plugins
    ```

## Installation of "jack_capture" 

1.  Make sure, that you are logged in with username `admin`.
1.  Install `jack_capture`.

```sh
cd ~  
wget http://deb.debian.org/debian/pool/main/j/jack-capture/jack-capture_0.9.73-3_arm64.deb  
sudo apt-get -y install ./jack-capture_0.9.73-3_arm64.deb
rm ./jack-capture_0.9.73-3_arm64.deb
```

    NOTE: If you see the notice that follows, ignore it:

```
Notice: Download is performed unsandboxed as root as file '/home/admin/jack-capture_0.9.73-3_arm64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```

## Disable swap file


```
sudo swapoff -a
```

(In a previous version we used `dphys-swapfile`. This is not needed.)
```
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo systemctl disable dphys-swapfile
sudo apt purge dphys-swapfile
```


## Auto remove not needed packages after installation

```
sudo apt-get -y autoremove
```


## Installation of the service "jackd.service"

1.  Make sure, that you are logged in with username `admin`.
1.  Do these modifications.

```
cd ~
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/jackd.service
```

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

### Enable, stop, start the service "jackd.service"

1.  Make sure, that you are logged in with username `admin`.
1.  Make sure, that you can start and stop the service "jackd.service".
1.  Do these steps.

```
systemctl --user daemon-reexec
systemctl --user daemon-reload

$
systemctl --user stop jackd.service
systemctl --user enable jackd.service
systemctl --user status jackd.service
systemctl --user start jackd.service
systemctl --user status jackd.service
```

    NOTE: It can be, that `status` will not show JACK started. Check with `ps aux | grep -i jack` and `jack_lsp` instead.

```
Created symlink '/home/admin/.config/systemd/user/default.target.wants/jackd.service' → '/home/admin/.config/systemd/user/jackd.service'.
○ jackd.service - JACK audio server (dummy backend)
     Loaded: loaded (/home/admin/.config/systemd/user/jackd.service; enabled; preset: enabled)
     Active: inactive (dead)
```

```
● jackd.service - JACK audio server (dummy backend)
     Loaded: loaded (/home/admin/.config/systemd/user/jackd.service; enabled; preset: enabled)
     Active: active (running) since Mon 2025-12-29 10:31:47 CET; 13ms ago
 Invocation: 44aa2f0d586a4bb8ad6c0252e0ab6665
   Main PID: 1293 ((jackd))
      Tasks: 1 (limit: 9573)
        CPU: 8ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/jackd.service
             └─1293 "(jackd)"

Dec 29 10:31:47 scnfmixr systemd[858]: Started jackd.service - JACK audio server (dummy backend).
```

## Installation of the "venv" of the service "scnfmixr.service"

1.  Make sure, that you are logged in with username `admin`.

1.  Make a Python "virtual environment".

```
mkdir -p ~/biz.dfch.scnfmixr
cd ~/biz.dfch.scnfmixr
python3 -m venv venv
source ~/biz.dfch.scnfmixr/venv/bin/activate
```

1.  Make sure, that the "virtual environment" is active.

1. Install the latest version of the "pip" package.

```
pip install --upgrade pip
```

1. Install necessary packages.

```
nano ./requirements.txt
```

```
pillow==12.0.0
streamdeck==0.9.8

```

```
pip install -r requirements.txt
```


## Installation of the service "scnfmixr.service"

1.  Make sure, that you are logged in with username `admin`.
1.  Make a directory on the Compute Module 5.

```
mkdir -p ~/biz.dfch.scnfmixr/src
```

1.  Make a local copy of the files from [biz.dfch.scnfmixr](https://github.com/dfensgmbh/biz.dfch.scnfmixr.git).

```
# Do this on the installation computer.
git clone .
```

1.  Make sure, that you can make an SSH connection to the Compute Module 5 with username `admin`.
1.  Install the files to the Compute Module 5 in the directory that follows.

```
# Source:
./src

# Target:
~/biz.dfch.scnfmixr/src
```

1.  Do these modifications.

```
cd ~
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/scnfmixr.service
```

```
[Unit]
Description=scnfmixr (Secure Conference Mixer and Recorder)
After=sound.target

[Service]
ExecStart=/home/admin/biz.dfch.scnfmixr/venv/bin/python3 -m biz -s -ex1 4-1.3 -ex2 4-1.2 -hi1 2-1.2 -hi 4-1.4 -lcl 2-1.3 -rc1 5-1.1 -rc2 3-1.1 --use-current-date --use-current-time --use-random-name --allowed-storage-usb-ids 2009 2d9b 058f:6387 0781:5591
WorkingDirectory=/home/admin/biz.dfch.scnfmixr/src
StandardOutput=journal
StandardError=journal
LimitRTPRIO=95
LimitMEMLOCK=infinity
LimitNICE=-10
Type=oneshot
Environment=TERM=dumb

[Install]
WantedBy=default.target

```

### Enable, stop, start the service "scnfmixr.service"

```
# Disable service.
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user disable scnfmixr.service
systemctl --user stop scnfmixr.service
systemctl --user daemon-reload

# Enable service.
systemctl --user enable scnfmixr.service
systemctl --user daemon-reload
systemctl --user start scnfmixr.service
systemctl --user status scnfmixr.service
journalctl -u scnfmixr.service
```

## Installation of the service "@mpd.service"

1.  Make sure, that you are logged in with username `admin`.
1.  Do these modifications.

```
# Create links for menu
mkdir -p ~/MpdMusic/menu
ln -s ~/biz.dfch.scnfmixr/src/biz/dfch/scnfmixr/res/EN ~/MpdMusic/menu/EN
ln -s ~/biz.dfch.scnfmixr/src/biz/dfch/scnfmixr/res/DE ~/MpdMusic/menu/DE
ln -s ~/biz.dfch.scnfmixr/src/biz/dfch/scnfmixr/res/FR ~/MpdMusic/menu/FR
ln -s ~/biz.dfch.scnfmixr/src/biz/dfch/scnfmixr/res/IT ~/MpdMusic/menu/IT

# Create links for playback
mkdir -p ~/MpdMusic/playback
sudo mkdir -p /mnt/rc1/
sudo mkdir -p /mnt/rc2/
ln -s /mnt/rc1 ~/MpdMusic/playback/rc1
ln -s /mnt/rc2 ~/MpdMusic/playback/rc2
```

```
cd ~
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/mpd@.service
```

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

### Installation of the service "mpd.playback"

```
mkdir -p ~/.config/mpd/menu/playlists
```

```
nano ~/.config/mpd/menu/mpd.conf
```

```
# Ensure, that within the directory below, links to the following directories are created:
# EN -> biz.dfch.scnfmixr/biz/dfch/scnfmixr/res/EN/
# DE -> biz.dfch.scnfmixr/biz/dfch/scnfmixr/res/DE/
# FR -> biz.dfch.scnfmixr/biz/dfch/scnfmixr/res/FR/
# IT -> biz.dfch.scnfmixr/biz/dfch/scnfmixr/res/IT/
music_directory    "~/MpdMusic/menu"

user	"admin"

playlist_directory "~/.config/mpd/menu/playlists"

db_file            "~/.config/mpd/menu/database"

log_file           "~/.config/mpd/menu/log"

pid_file           "~/.config/mpd/menu/pid"

state_file         "~/.config/mpd/menu/state"

sticker_file       "~/.config/mpd/menu/sticker.sql"

bind_to_address    "/run/user/1000/mpd.menu.socket"

audio_output {
	type		"jack"
	name		"system"
	client_name	"Mpd:Menu"
	source_ports	"capture_1,capture_2"
	destination_ports	"Alsa:LCL-O:playback_1,Alsa:LCL-O:playback_2"
	auto_destination_ports	"yes"
}
```

### Installation of the service "mpd.menu"

```
mkdir -p ~/.config/mpd/playback/playlists
```

```
nano ~/.config/mpd/playback/mpd.conf
```

```
# Ensure, that within the directory below, links to the following directories are created:
# rc1 - > /mnt/rc1
# rc2 - > /mnt/rc2
music_directory    "~/MpdMusic/playback"

user	"admin"

playlist_directory "~/.config/mpd/playback/playlists"

db_file            "~/.config/mpd/playback/database"

log_file           "~/.config/mpd/playback/log"

pid_file           "~/.config/mpd/playback/pid"

state_file         "~/.config/mpd/playback/state"

sticker_file       "~/.config/mpd/playback/sticker.sql"

bind_to_address    "/run/user/1000/mpd.playback.socket"

audio_output {
	type		"jack"
	name		"system"
	client_name	"Mpd:Playback"
	source_ports	"capture_1,capture_2"
	destination_ports	"Alsa:LCL-O:playback_1,Alsa:LCL-O:playback_2"
	auto_destination_ports	"yes"
}
```

### Enable, stop, start the service "@mpd.service"

```
systemctl --user daemon-reexec
systemctl --user daemon-reload

systemctl --user stop --now mpd@playback.service
systemctl --user enable --now mpd@playback.service
systemctl --user start --now mpd@playback.service
systemctl --user status --now mpd@playback.service

systemctl --user stop --now mpd@menu.service
systemctl --user enable --now mpd@menu.service
systemctl --user start --now mpd@menu.service
systemctl --user status --now mpd@menu.service

systemctl --user daemon-reload
```


#### Testing the service "@mpd.service"

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

# Hardening

These are the steps for "Hardening" the system:

## Boot order

Make sure, that the system only starts from internal eMMC. See [BOOT_ORDER](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#BOOT_ORDER) for more information.

NOTE: This is a CM5 "Lite" Compute Module. This Compute Module has integrated eMMC. The external SD card will not operate.

First, make sure that the `firmware` partition is read-write:

```sh
sudo mount -o remount,rw /boot/firmware
```

```sh
sudo rpi-eeprom-config --edit

[all]
BOOT_ORDER=0xf16
```

## Power settings

First, make sure that the `firmware` partition is read-write:

```sh
sudo mount -o remount,rw /boot/firmware
```

```sh
$ sudo rpi-eeprom-config --edit

[all]  
PSU_MAX_CURRENT=5000
```

Make sure that you get this output after you started the CM5 again:

```sh
$ vcgencmd get_config usb_max_current_enable
usb_max_current_enable=1

$ vcgencmd get_throttled
throttled=0x0
```

## `pi` user account

Make sure, that there is no `pi` user account.

```sh
id pi
```

If there is a `pi` user account, remove the user account.

## `root` user account

Make sure, that the `root` account is not active and that the account cannot login.

```sh
$ sudo passwd -l root
$ sudo vipw

root:x:0:0:root:/root:/bin/bash
```

Make sure, that the `root` user account has no password.

```sh
$ sudo cat /etc/shadow | grep -i root
root:!*:19747:0:99999:7:::
     ^
$ sudo passwd -S root

root L 2025-01-01 0 99999 7 -1
     ^
```

## `admin` user account

Make sure, that the `admin` user account has a strong password.

## Disable automatic mount of storage

```sh
$ sudo systemctl disable --now systemd-udev-trigger
```

NOTE: USB storage devices load with `noexec,nodev,nosuid`

## Disable wired network connection `eth0`

```sh
$ sudo nano /etc/NetworkManager/conf.d/unmanaged-eth0.conf
```

```
[keyfile]
unmanaged-devices=interface-name:eth0
```

```
$ sudo reboot
```

### Disable when overlay-fs is active

```sh
sudo nano /mnt/writable_disk/etc/NetworkManager/conf.d/unmanaged-eth0.conf
```

```
<same service as above>
```

```
$ sudo reboot
```

## Allow only specific USB devices

### USB network device blacklist

```sh
sudo nano /etc/udev/rules.d/10-usb-network-blacklist.rules

# On overlay-fs:
# sudo mount -o remount,rw /media/root-ro
# sudo nano /media/root-ro/etc/udev/rules.d/10-usb-network-blacklist.rules
```

```sh
# 10-usb-network-blacklist.rules
# Block any USB device exposing a network-related interface (CDC / wireless).

# Match USB interfaces with Communication (0x02) class
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ACTION=="add", ATTR{bInterfaceClass}=="02", \
  RUN+="/bin/sh -c 'echo -n %b > /sys/bus/usb/drivers/usb/unbind; /usr/bin/logger -t usb-net-deny \"BLOCKED USB network-like interface: %k on device %b (class=02)\"'"

# Match USB interfaces with Wireless Controller (0x0e) class
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ACTION=="add", ATTR{bInterfaceClass}=="0e", \
  RUN+="/bin/sh -c 'echo -n %b > /sys/bus/usb/drivers/usb/unbind; /usr/bin/logger -t usb-net-deny \"BLOCKED USB network-like interface: %k on device %b (class=0e)\"'"

```

### USB device whitelist

```sh
$ sudo nano /etc/udev/rules.d/20-usb-device-whitelist.rules

# On overlay-fs:
# sudo mount -o remount,rw /media/root-ro
# sudo nano /media/root-ro/etc/udev/rules.d/20-usb-device-whitelist.rules
```

```sh
# 20-usb-device-whitelist.rules
# Allow only the USB devices that are listed below.
# Any other USB device is immediately unbound from the kernel driver.

# ----------------------------
# 1. Allowlist (by VID:PID)
# ----------------------------

# Linux Foundation root hubs
SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0002", GOTO="usb_whitelist_end"
SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0003", GOTO="usb_whitelist_end"

# Raspberry Pi USB3 HUBs
SUBSYSTEM=="usb", ATTR{idVendor}=="2e8a", ATTR{idProduct}=="000d", GOTO="usb_whitelist_end"
SUBSYSTEM=="usb", ATTR{idVendor}=="2e8a", ATTR{idProduct}=="000e", GOTO="usb_whitelist_end"

# EPOS EXPAND 40T (DSEA A/S), LCL
SUBSYSTEM=="usb", ATTR{idVendor}=="1395", ATTR{idProduct}=="0386", GOTO="usb_whitelist_end"

# Homertech USB Keyboard, HI1
SUBSYSTEM=="usb", ATTR{idVendor}=="276d", ATTR{idProduct}=="ffe3", GOTO="usb_whitelist_end"

# Elgato Stream Deck MK.2, HI2
SUBSYSTEM=="usb", ATTR{idVendor}=="0fd9", ATTR{idProduct}=="0080", GOTO="usb_whitelist_end"

# iStorage datAshur PRO2, RC1, RC2
SUBSYSTEM=="usb", ATTR{idVendor}=="2d9b", ATTR{idProduct}=="8064", GOTO="usb_whitelist_end"

# C-Media Audio Adapter (Unitek Y-247A), EX1, EX2
SUBSYSTEM=="usb", ATTR{idVendor}=="0d8c", ATTR{idProduct}=="0014", GOTO="usb_whitelist_end"

# Genesys Logic Hub (part of Pi Keyboard)
SUBSYSTEM=="usb", ATTR{idVendor}=="05e3", ATTR{idProduct}=="0610", GOTO="usb_whitelist_end"

# Holtek RPI Wired Keyboard 5
SUBSYSTEM=="usb", ATTR{idVendor}=="04d9", ATTR{idProduct}=="0006", GOTO="usb_whitelist_end"

# PI Engineering, Inc. XK-24 HID
SUBSYSTEM=="usb", ATTR{idVendor}=="05f3", ATTR{idProduct}=="0405", GOTO="usb_whitelist_end"

# Roland Corp. VT-4
SUBSYSTEM=="usb", ATTR{idVendor}=="0582", ATTR{idProduct}=="021a", GOTO="usb_whitelist_end"

# Allow any USB Mass Storage device (class 08) regardless of VID:PID
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{bDeviceClass}=="08", GOTO="usb_whitelist_end"

# Allow USB devices where any interface is Mass Storage (class 08)
# (covers composite devices that expose storage as one of their interfaces)
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ATTR{bInterfaceClass}=="08", GOTO="usb_whitelist_end"

# ---------------------------------
# 2. Default DENY: unbind everything else
# ---------------------------------
# For any USB device (not interface) that reaches here (i.e. not whitelisted),
# unbind it from the USB core driver and log the event.

SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ACTION=="add", \
  RUN+="/bin/sh -c 'echo -n %k > /sys/bus/usb/drivers/usb/unbind; /usr/bin/logger -t usb-whitelist \"BLOCKED USB device: %k VID=%s{idVendor} PID=%s{idProduct}\"'"

LABEL="usb_whitelist_end"

```

### USB class blacklist

```sh
sudo nano /etc/udev/rules.d/15-usb-class-blacklist.rules

# On overlay-fs:
# sudo mount -o remount,rw /media/root-ro
# sudo nano /media/root-ro/etc/udev/rules.d/15-usb-class-blacklist.rules
```

```sh
# 15-usb-class-blacklist.rules
# Block any USB device that exposes an interface class OTHER than:
#   01 (Audio), 03 (HID), 08 (Mass Storage), 09 (Hub)

# Allow hubs (class 09) at device level - they are infrastructure
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{bDeviceClass}=="09", GOTO="usb_class_deny_end"

# For interfaces: allow only 01, 03, 08, 09
# Use %b (parent device bus path) not %k (interface name) for unbind
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ACTION=="add", \
  ATTR{bInterfaceClass}!="01", \
  ATTR{bInterfaceClass}!="03", \
  ATTR{bInterfaceClass}!="08", \
  ATTR{bInterfaceClass}!="09", \
  RUN+="/bin/sh -c 'echo -n %b > /sys/bus/usb/drivers/usb/unbind; /usr/bin/logger -t usb-class-deny \"BLOCKED USB interface class: %k on device %b\"'"

LABEL="usb_class_deny_end"

```

### Activate rules

```sh
$ sudo udevadm control --reload
$ sudo udevadm trigger
```

### Test rules

```sh
# Test 20 rule with a device on 4-1.4
sudo udevadm test /sys/bus/usb/devices/4-1.4 2>&1 | grep -E '20-usb-device-whitelist|RUN'
sudo journalctl -t usb-whitelist --since -2m
```

## Prepare for golden image

```sh
systemctl --user stop scnfmixr.service &

systemctl --user stop mpd@playback.service
systemctl --user stop mpd@menu.service
rm ~/.config/mpd/menu/database
rm ~/.config/mpd/playback/database

systemctl --user stop jackd.service
rm ~/biz.dfch.scnfmixr/src/app.log
```

## Clean the logs

```sh
sudo truncate -s 0 /var/log/auth.log
sudo truncate -s 0 /var/log/syslog

sudo truncate -s 0 /var/log/btmp
sudo truncate -s 0 /var/log/wtmp
sudo truncate -s 0 /var/log/lastlog

sudo journalctl --vacuum-time=1s

history -c
history -w
```

## Enable filesystem overlay

```sh
sudo raspi-config

# In "Performance" options, enable the file system overlay.
# Make sure, that the "boot partition" is read-only.
sudo reboot
```


# Prerequisites

## Installation of "rpiboot-CM4-CM5 - Mass Storage Gadget" (RPIBOOT)

### Windows

```sh
34404893 Oct 27 16:00 rpiboot_setup.exe
c967a17818f509f06e85921c604b8fe93f0ff98048253658e0182bc2c4e4bf8a  rpiboot_setup.exe
```

```sh
817445 May 19  2025 rpiboot.exe
69138d0ceef7b35a7610f5202c1852d04523fe87b44afe3c95b35c1ac40488e5  rpiboot.exe
```

## Installation of "Raspberry Pi Imager" v1.9.6 (RPIIMAGER)

```sh
Raspberry Pi Imager v1.9.6
```

# Checklist to install a new system

## Install new eMMC
 
1. Start with NVMe
Mount the NVMe disk in the case.

2. Connect with Putty

3. Write image to disk
cd Desktop
./write.sh

4. Change EEPROM BOOT_ORDER and PSU_MAX_CURRENT
sudo mount -o remount,rw /boot/firmware
sudo rpi-eeprom-config --edit

BOOT_ORDER=0xf16
PSU_MAX_CURRENT=5000
 
Make sure, there is a "NEWLINE" after "5000".
Do this step in parallel to the previous step.

5. Set USB maximum current to "1"
vcgencmd get_config usb_max_current_enable
echo "usb_max_current_enable=1" | sudo tee -a /boot/firmware/config.txt
vcgencmd get_config usb_max_current_enable

6. When write is complete, stop the system.
sudo poweroff

7. Remove NMVe Disk
WARNING: When you remove the NVMe disk, make sure the system has no power.
 
8. Start the system

9. Connect with Putty

10. Make disk writable
sudo mkdir -p /mnt/writable_disk
sudo mount /dev/mmcblk0p2 /mnt/writable_disk/
sudo mount -o remount,rw /dev/mmcblk0p2 /mnt/writable_disk/

11. Stop scnfmixr service
systemctl --user stop scnfmixr.service

12. Write scnfmixr service with WinSCP
  * Use Transfer Settings __pycache__.

13. Change ExecStart
nano /mnt/writable_disk/home/admin/.config/systemd/user/scnfmixr.service

ExecStart=/home/admin/PhoneTap/venvpi/bin/python3 -m biz -s -ex1 2-1.1 -hi2 2-1.4 -lcl 4-1 -rc1 3-1.2 -rc2 3-1.3 --allowed-storage-usb-ids 2009 2d9b 0781:5591

Remove all other "ExecStart" entries.

14. When write scnfmixr.service (in WinSCP) is complete, refresh WinSCP and make sure there is no "app.log".

15. Stop the system
sudo poweroff

NOTE: When you stop the system with `sudo poweroff` it can take more than 3 minutes before the system starts again.

16. Connect these devices:
  * LCL
  * HI2
  * EX1
  * RC1
  * RC2.

17. Remove the power button from the IO Board

NOTE: Remove the grey power button with a "Knipex Schrägabschneider".

17. Start the system

18. Make sure, the system operates correctly.

19. Do the test procedure "NNN".

## Deployment of "Golden Image"

|   | 1                  | 2                | 3                   | 4                      |
|---|--------------------|------------------|---------------------|------------------------|
| A | old                |                  | new                 |                        |
| B | Console 1          | Console 2        | Enable network 1    | Enable network 2       |
| C | Enable writable 1  | Enable writable 2| Enable writable 3   | Stop scnfmixr.service  |
| D | ExecStart          | IP address       | Write Image to eMMC | Reboot                 |
| E | Prepare boot order | Edit boot order  | BOOT ORDER FINAL    | USB CURRENT            |
| F |                    |                  | BOOT ORDER USB      |                        |

**Explanation:**  
- <B3>: "Enable network 1"

### Use cases

#### Login to "Golden Image"  

<A3> <A4>

#### Login to Deployment OS on USB memory stick or existing scnfmixr  

<A1> <A2>

#### Prepare system with overlay-fs for changes

<C1> <C2> <C3> <C4>

* The last command stops the `scnfmixr.service`. This takes 90 seconds. Change to a different console after that to continue your work.

#### Change to console 1

<B1>

#### Change to console 2

<B2>

#### Change boot order

<E1> <E2>

Then change settings with <E3> and <E4> or <F3>.

<E3>: insert the boot order to NVMe -- > SD/eMMC -- > retry
<F3>: insert the boot order to USB -- > NVMe -- > SD/eMMC -- > retry
<E4>: add setting for USB PSU at 5A

#### Restart system

<D4>

NOTE: stop `scnfmixr.service` with <C4> before you restart the system. This will save time when the system stops.

#### Write "Golden Image" to eMMC

<D3>

This will write the "Golden Image" directly to the eMMC storage device. You must restart the system after that. Also adjust the boot order if you want to start from the eMMC storage device after you have written "Golden Image" to it.

### Deploy a "Golden Image" on an existing system

 1) Connect the USB storage device with "Golden Image".
 2) Connect the monitor with an HDMI cable.
 3) Connect the Raspberry keyboard and X-Keys keyboard.
 4) Connect the power cord and start system.
 5) Login to system.
    * <A3> <A4>
 6) Prepare system for changes.
    * <C1> <C2> <C3> <C4>
    NOTE: The last command will stop the `scnfmixr.service`. This will take 90s.
 7) Change to console 2.
    * <B2>
 8) Login to system.
    * <A3> <A4>
 9) Change boot order.
    * <E1> <E2>
    * Remove existing entry BOOT_ORDER with CTRL+K.
    * Add BOOT_ORDER.
    * <F3>
    * Save file and exit with CTRL+O und CTRL+X.
    * Examine that the flash operation is "SUCCESSFUL".
10) Change to console 1.
    * <B1>
11) Restart the system.
    * <D4>
    NOTE: If the `scnfmixr.service` has not stopped, wait until it has stopped. The system stops will then stop and start again.
12) Continue with procedure 'Deploy a "Golden Image" on a new system' step (5).

### Change files on an existing system

 1) Connect the USB storage device with "Golden Image".
 2) Connect the monitor with an HDMI cable.
 3) Connect the Raspberry keyboard and X-Keys keyboard.
 4) Connect the power cord and start system.
 5) Connect a network cable to the system.
 6) Login to system.
    * <A3> <A4>
 7) Prepare system for changes.
    * <C1> <C2> <C3> <C4>
    NOTE: The last command will stop the `scnfmixr.service`. This will take 90s.
 8) Change to console 2.
    * <B2>
 9) Login to system.
    * <A3> <A4>
10) Enable network.
    * <B3> <B4>
11) Show IP configuration and record IP address.
    * <D2>
12) Use the IP address from the previous step and continue with procedure 'Changing files with WinSCP'. After you finished that procedure continue with step (13).

### Deploy a "Golden Image" on a new system

 1) Connect the USB storage device with "Golden Image".
 2) Connect the monitor with an HDMI cable.
 3) Connect the Raspberry keyboard and X-Keys keyboard.
 4) Connect the power cord and start system.
 5) Login to system.
    * <A1> <A2>
 6) Write "Golden Image" from USB storage device to eMMC storage device.
    * <D3>
 7) Change to console 2.
    * <B2>
 8) Login to system.
    * <A1> <A2>
 9) Change boot order.
    * <E1> <E2>
    * Remove existing entry BOOT_ORDER with CTRL+K.
    * Add BOOT_ORDER and PSU_MAX_CURRENT.
    * <E3> <E4>
    * Save file and exit with CTRL+O und CTRL+X.
    * Examine that the flash operation is "SUCCESSFUL".
10) Change to console 1.
    * <B1>
11) Wait until the write operation is completed.
    NOTE: The write operation will take approximately 85 seconds.
12) Restart the system.
    * <D4>
    NOTE: Keep the USB storage device in the system.
---
13) Login to system.
    * <A3> <A4>
    NOTE: If we can login to the system successfully, we show that the system does not start from USB any more.
14) Prepare system for changes.
    * <C1> <C2> <C3> <C4>
    NOTE: The last command will stop the `scnfmixr.service`. This will take 90s.
15) Change to console 2.
    * <B2>
16) If the system is a "REC" system continue with step (22).
17) Change ExecStart.
    * <D1>
    NOTE: This will start the text editor with the start configuration of the `scnfmixr.service`.
18) Comment out the line that starts with `ExecStart` and insert "#" at the start of the line.
19) When the system is "playback system" ("PLY"), find the line that starts with `#ExecStart=` after the line that contains "PLY". Remove the "#" at the start of the line.
20) When the system is "multi-phone system with insert" ("LIN"), find the line that starts with `#ExecStart=` after the line that contains "LIN". Remove the "#" at the start of the line.
21) Save the changes you made and exit the editor with CTRL+O CTRL+X.
22) Change to console 1.
    * <B1>
23) Remove the USB storage device.
24) Restart the system.
    * <D4>
    NOTE: If the `scnfmixr.service` has not stopped, wait until it has stopped. The system stops will then stop and start again.
---
25) Login to system.
    * <A3> <A4>
26) Prepare system for changes.
    * <C1> <C2> <C3> <C4>
    NOTE: The last command will stop the `scnfmixr.service`. This will take 90s.
27) Change to console 2.
    * <B2>
28) Open ExecStart.
    * <D1>
    NOTE: This will start the text editor with the start configuration of the `scnfmixr.service`.
29) Make sure that the correct `ExecStart=` line is active.
30) Change to console 1.
    * <B1>
31) Restart the system.
    * <D4>
    NOTE: If the `scnfmixr.service` has not stopped, wait until it has stopped. The system stops will then stop and start again.
32) When the system starts again, remove the power cord from the system.
