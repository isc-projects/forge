#!/bin/bash
# This script is used to install the Incus application on a fresh debian 12 instance

export LANGUAGE="C"
export LC_ALL="C"
sudo apt update 
sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y
sudo apt install incus jq -y
sudo adduser "$(whoami)" incus-admin
newgrp incus-admin 
# for some reason script ends here, run the following commands manually
incus admin init --auto
#--storage-backend=zfs
incus admin init --dump
