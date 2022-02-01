#!/bin/bash
set -e -x

# WA for missing /dev/ptmx on Ubuntu LXC in AWS Jenkins
if [ ! -e /dev/ptmx ]; then
    sudo ln -s /dev/pts/ptmx /dev/ptmx
    sudo systemctl restart systemd-resolved
fi

# disable apt updates to not lock it
sudo systemctl stop apt-daily-upgrade.timer apt-daily.timer
sudo systemctl disable apt-daily-upgrade.timer apt-daily.timer
sudo systemctl stop apt-daily.service apt-daily-upgrade.service
sudo systemctl disable apt-daily.service apt-daily-upgrade.service

sudo apt update
ps axf
sudo DEBIAN_FRONTEND=noninteractive apt install -o Dpkg::Options::="--force-all" -y python3 python3-venv g++ python3-dev libpcap-dev git

rm -rf $HOME/venv
python3 -m venv $HOME/venv
$HOME/venv/bin/pip install -U pip
$HOME/venv/bin/pip install -r /forge/requirements.txt


# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::/64 dev enp0s9
