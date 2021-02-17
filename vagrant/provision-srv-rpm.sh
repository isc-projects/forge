#!/bin/bash
set -e -x

sudo dnf install -y socat freeradius bind net-tools tcpdump

# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::1000/64 dev enp0s9

# enable access to pgsql
sudo sed -i -e s/ident/md5/ /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
