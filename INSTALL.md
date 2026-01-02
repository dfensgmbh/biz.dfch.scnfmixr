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
