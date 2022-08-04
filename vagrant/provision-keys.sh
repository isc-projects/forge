#!/bin/bash
set -e -x

if [ ! -f $HOME/.ssh/authorized_keys.orig ]; then
    cp $HOME/.ssh/authorized_keys $HOME/.ssh/authorized_keys.orig
fi
cp $HOME/.ssh/authorized_keys.orig $HOME/.ssh/authorized_keys
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9k+O9Jzl3906khOTFWJEBoH+NGAf8wTJOPjvgi7XvbI/CRCddyHMkjtcRpB7rQYHXzHoFjVcTZZDdpkDofY4pHYQZEPYKnrPYjlNCV6ps1yrsHYbvEnbwvvscYaBm7JSftn+sAxRZPS2qI4nZsbzeVqCbt91Y6pbruEuhoKBWGvHDbE19PQeRTc/+XpTywdiZgKSawEnUxSVXjwrOP/+wNRu9J6zdQM8LxJBQX2pqtusnHT48+QebO+bP/njmUldWJRow0MCmuaFTKVcOoTknvRz7Oml4qOKt1WLqKpEkVG3GNUCPWdQHF1g90EXRPQhGamuPzM34LNNltUlFcWuP godfryd@u-1810-kea-cli" >> $HOME/.ssh/authorized_keys
chmod 600 $HOME/.ssh/id_rsa
