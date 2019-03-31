#!/bin/bash
set -e -x

if [ ! -f $HOME/.ssh/authorized_keys.orig ]; then
    cp $HOME/.ssh/authorized_keys $HOME/.ssh/authorized_keys.orig
fi
cp $HOME/.ssh/authorized_keys.orig $HOME/.ssh/authorized_keys
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9k+O9Jzl3906khOTFWJEBoH+NGAf8wTJOPjvgi7XvbI/CRCddyHMkjtcRpB7rQYHXzHoFjVcTZZDdpkDofY4pHYQZEPYKnrPYjlNCV6ps1yrsHYbvEnbwvvscYaBm7JSftn+sAxRZPS2qI4nZsbzeVqCbt91Y6pbruEuhoKBWGvHDbE19PQeRTc/+XpTywdiZgKSawEnUxSVXjwrOP/+wNRu9J6zdQM8LxJBQX2pqtusnHT48+QebO+bP/njmUldWJRow0MCmuaFTKVcOoTknvRz7Oml4qOKt1WLqKpEkVG3GNUCPWdQHF1g90EXRPQhGamuPzM34LNNltUlFcWuP godfryd@u-1810-kea-cli" >> $HOME/.ssh/authorized_keys

sudo apt update
sudo apt install -y python python-virtualenv g++ python-dev libpcap-dev

if ! ifconfig | grep '2001:db8:0:f102::1'; then
    sudo ip -6 addr add 2001:db8:0:f102::1/64 dev enp0s9
fi
if ! ifconfig | grep '2001:db8:1:f102::1'; then
    sudo ip -6 addr add 2001:db8:1:f102::1/64 dev enp0s10
fi

rm -rf $HOME/venv
python -m virtualenv $HOME/venv
$HOME/venv/bin/pip install -U pip
$HOME/venv/bin/pip install -r /forge/requirements.txt
