#!/bin/bash
set -e -x

sudo apk update
sudo apk add socat gnupg bind net-tools tcpdump freeradius

# this is needed for ddns tests
sudo ip -6 route add 2001:db8:1::/64 dev enp0s9
