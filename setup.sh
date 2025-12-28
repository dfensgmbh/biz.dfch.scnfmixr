#!/bin/bash
set -e

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Default installation directory.
DEFAULT_INSTALL_PATH="/opt/PhoneTap"

# Input parameters:
# $1 INSTALL_PATH
# $2 SRC_FILE
INSTALL_PATH="${1:-$DEFAULT_INSTALL_PATH}"
SRC_FILE="$2"

# Check if SRC_FILE has been specified.
if [[ -z "$SRC_FILE" ]]; then
  echo "ERROR: 'arg2' not specified. You must provide the path to the .whl file."
  echo "Usage: $0 [INSTALL_PATH] /path/to/PhoneTap.whl"
  exit 1
fi

# Check if specified .whl file exists.
if [[ ! -f "$SRC_FILE" ]]; then
  echo "ERROR: '$SRC_FILE' does not exist. You must provide the path to the .whl file."
  echo "Usage: $0 [INSTALL_PATH] /path/to/PhoneTap.whl"
  exit 1
fi

# Check if installation directory already exists.
if [[ -e "$INSTALL_PATH" ]]; then
  echo "ERROR: Installation directory '$INSTALL_PATH' already exists. Aborting ..."
  exit 1
fi

VENV_DIR="$INSTALL_PATH/venv"
SYSTEMD_SERVICE_NAME="PhoneTap.service"
SYSTEMD_SERVICE_PATH="/etc/systemd/system/${SYSTEMD_SERVICE_NAME}"

echo "Installing to target: $INSTALL_PATH."
echo "Virtual environment will be created at: $VENV_DIR."
echo "Installing wheel from source: $SRC_FILE."

# Create installation directory.
echo "Creating installation directory ..."
sudo mkdir -p "$INSTALL_PATH"

echo "Setting permissions for current user ..."
sudo chown -R "$USER":"$USER" "$INSTALL_PATH"

echo "Creating virtual environment '$VENV_DIR' ..."
python3 -m venv "$VENV_DIR"

echo "Changing directory to virtual environment '$VENV_DIR' ..."
cd "$VENV_DIR"

echo "Activating virtual environment ..."
source "$VENV_DIR/bin/activate"
echo "Upgrading pip ..."
# pip install --upgrade pip
echo "Installing package ..."
pip install "$SRC_FILE"
echo "Deactivating virtual environment ..."
deactivate

if [[ ! -f "$INSTALL_PATH/app.service" ]]; then
  echo "ERROR: Service file '$INSTALL_PATH/app.service' not found. Aborting ..."
  exit 1
fi
echo "Creating symbolic link '$SYSTEMD_SERVICE_PATH' for service '$INSTALL_PATH/app.service' ..."
sudo ln -sf "$INSTALL_PATH/app.service" "$SYSTEMD_SERVICE_PATH"

echo "Reloading systemd ..."
sudo systemctl daemon-reload
echo "Enabling service ..."
sudo systemctl enable "$SYSTEMD_SERVICE_NAME"
echo "Starting service ..."
sudo systemctl start "$SYSTEMD_SERVICE_NAME"

echo "Setup completed successfully."
