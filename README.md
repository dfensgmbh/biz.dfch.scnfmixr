# biz.dfch.PhoneTap
PhoneTap running on Raspberry Pi OS (Pi 5)

# Installation

```python

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
