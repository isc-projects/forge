#!/bin/bash
# This script is used to install the Incus application on a fresh debian 12 instance

set -eu

export LANGUAGE="C"
export LC_ALL="C"

# Install incus.
if command -V apt > /dev/null 2>&1; then
  sudo apt update
  sudo apt install incus jq -y
fi

# Add user to group.
sudo usermod -aG incus-admin "${USER}"

# Initialize incus.
echo "incus admin init --auto; incus admin init --dump" | newgrp incus-admin > /dev/null

line='root:1000000:1000000000'
for i in /etc/subuid /etc/subgid; do
  if ! grep -F "${line}" "${i}" > /dev/null; then
    sudo echo "${line}" >> "${i}"
  fi
done

systemctl restart incus

# "incus admin init --auto" should have already done these actions, but in some cases it says
# "manual confgiuration is required", so if not done, let us do them ourselves.
if ! ip a s incusbr0 > /dev/null 2>&1; then
  sudo incus network create incusbr0 ipv4.address=192.168.100.1/24 ipv6.address=2001:db0::1/32 ipv4.nat=yes ipv6.nat=yes ipv4.dhcp=yes ipv4.dhcp.ranges=192.168.100.1-192.168.100.100 ipv4.dhcp.gateway=192.168.100.1
fi
if ! sudo incus profile device list default | grep eth0 > /dev/null; then
  sudo incus profile device add default eth0 nic nictype=bridged parent=incusbr0
fi
if ! sudo incus profile device list default | grep root > /dev/null; then
  sudo incus profile device add default root disk path=/ pool=default
fi

# Show incus config.
incus admin init --dump
