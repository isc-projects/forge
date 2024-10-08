#!/bin/bash
# This script is used to install the Incus application on a fresh debian 12 instance

export LANGUAGE="C"
export LC_ALL="C"
sudo apt update 
sudo apt install incus jq -y
sudo adduser "${USER}" incus-admin
echo "incus admin init --auto; incus admin init --dump" | newgrp incus-admin