#!/bin/bash
set -e -x

sudo dnf install -y socat freeradius bind net-tools tcpdump

# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::/64 dev enp0s9

# Generate certificates for the FreeRADIUS server.
sudo /etc/raddb/certs/bootstrap
