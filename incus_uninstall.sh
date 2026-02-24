#!/bin/sh

# Uninstalls incus settings. Useful to prepare for re-running incus_install.sh.

set -eu

if sudo incus profile device list default | grep eth0 > /dev/null; then
  sudo incus profile device remove default eth0
fi
if sudo incus profile device list default | grep root > /dev/null; then
  sudo incus profile device remove default root
fi
if ip a s incusbr0 > /dev/null 2>&1; then
  sudo incus network delete incusbr0
fi
