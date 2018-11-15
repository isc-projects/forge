#!/usr/bin/env bash

# Copyright (C) 2015-2017 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Włodzimierz Wencel

revert_addr() {
    IFS='.' read -ra ADDR <<< $1
    for i in "${ADDR[@]}"; do
        revert=$i"."$revert
    done
    echo $revert
}

mask2cidr() {
    nbits=0
    IFS=.
    for dec in $1 ; do
        case $dec in
            255) let nbits+=8;;
            254) let nbits+=7;;
            252) let nbits+=6;;
            248) let nbits+=5;;
            240) let nbits+=4;;
            224) let nbits+=3;;
            192) let nbits+=2;;
            128) let nbits+=1;;
            0);;
            *) echo "Error: new netmask not valid!"; exit 1
        esac
    done
    echo "$nbits"
}

changeaddress() {
    read -p "Are you sure? [Yy]" -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        cd $1
        for file_name in $(find `pwd` -type f -name "*.feature");
        do
            # make backup if there is none
            tmp=$file_name
            tmp+="_BACKUP"
            cp -n $file_name $tmp

            # Changing address
            printf "\nChanging file: %s" $file_name
            mask=$(mask2cidr $3)

            sed -i "s/$4.0\/24/$2.0\/$mask/" $file_name
            sed -i "s/$5/$3/" $file_name

            default_revert=$(revert_addr $4)
            new_revert=$(revert_addr $2)

            sed -i "s/$default_revert/$new_revert/" $file_name
            sed -i "s/$4/$2/g" $file_name
        done
        printf "\n"
    else
        printf "\nAbording..\n"
        exit 0
    fi
}

restore_files(){
    read -p "Are you sure? [Yy]" -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        cd $1
        for file_name in $(find `pwd` -type f -name "*_BACKUP");
        do
            printf "\nRestoring file: %s" ${file_name::-7}
            mv -f $file_name ${file_name::-7}
        done
        printf "\n"
    else
        printf "\nAbording..\n"
        exit 0
    fi
}

## main

if [ "$1" == --help -o "$1" == -h ]; then
    #TODO: write help here
    printf "That script will be an interactive configuration of Forge.\nTo change default settings:
    ./modify_address -d <path_to_test_dir> <new_subnet_addr_3_octets> <new_netmask>
to change addresses that are not default:
    ./modify_address -s <path_to_test_dir> <new_subnet_addr_3_octets> <new_netmask>\
 <old_subnet_addr_3_octets> <old_netmask>\nIf you want to restore tests form backup files:
    ./modify_address -r <path_to_directory>\n"
    exit 0

elif [ "$1" == --default-addr -o "$1" == -d ]; then
    default_address="192.168.50"
    default_netmask="255.255.255.0"
    printf "You are about to change all tests in path: %s" $2
    printf "\nYour variables are:\nNew address: %s\nNew netmask: %s\n" $3 $4
    changeaddress $2 $3 $4 $default_address $default_netmask
    exit 0

elif [ "$1" == --switch-addr -o "$1" == -s ]; then
    printf "You are about to change all tests in path: %s" $2
    printf "\nYour variables are:\nOld subnet address: %s\nNew subnet address: %s\n" $5 $3
    printf "Old netmask: %s\nNew netmask: %s\n" $6 $4
    changeaddress $2 $3 $4 $5 $6
    exit 0

elif [ "$1" == --switch-str -o "$1" == -st ]; then
    printf "You are about to change all FILES in path: %s" $2
    printf "\nYour variables are:\nOld subnet address: %s\nNew subnet address: %s\n" $5 $3
    printf "\nYou are about to change string: %s\nTo: %s\n" $5 $3
    changestr $2 $3
    exit 0


elif [ "$1" == --restore-addr -o "$1" == -r ]; then
    printf "You are about to restore backuped tests features in directory: %s\nAll previous changes will be lost!\n" $2
    restore_files $2
    exit 0

else
    printf "Choose first argument from: --help -h; --default -d; --switch -s; --restore -r\n"
    exit 0

fi

