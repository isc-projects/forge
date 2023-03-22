#!/bin/bash
set -e -x

sudo apk update
sudo apk add -y socat gnupg  net-tools tcpdump

#freeradius bind9

# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::/64 dev enp0s9
