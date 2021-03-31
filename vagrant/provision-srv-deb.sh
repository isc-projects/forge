#!/bin/bash
set -e -x

# WA for missing /dev/ptmx on Ubuntu LXC in AWS Jenkins
if [ ! -e /dev/ptmx ]; then
    sudo ln -s /dev/pts/ptmx /dev/ptmx
fi

# disable apt updates to not lock it
sudo systemctl stop apt-daily-upgrade.timer apt-daily.timer
sudo systemctl disable apt-daily-upgrade.timer apt-daily.timer
sudo systemctl stop apt-daily.service apt-daily-upgrade.service
sudo systemctl disable apt-daily.service apt-daily-upgrade.service

sudo apt update
sudo apt install -y socat gnupg freeradius bind9 net-tools tcpdump

# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::1000/64 dev enp0s9
