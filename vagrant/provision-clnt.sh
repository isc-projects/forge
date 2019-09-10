#!/bin/bash
set -e -x

sudo systemctl stop apt-daily-upgrade.timer apt-daily.timer
sudo systemctl disable apt-daily-upgrade.timer apt-daily.timer
sudo systemctl stop apt-daily.service apt-daily-upgrade.service
sudo systemctl disable apt-daily.service apt-daily-upgrade.service

sudo apt update
ps axf
sudo apt install -y python python-virtualenv g++ python-dev libpcap-dev git

rm -rf $HOME/venv
python -m virtualenv $HOME/venv
$HOME/venv/bin/pip install -U pip
$HOME/venv/bin/pip install -r /forge/requirements.txt
