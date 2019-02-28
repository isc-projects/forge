#!/bin/bash

#Author: Maciek Fijalkowski

path=$(pwd)

if [ "$1" == --help -o "$1" == -h ]; then
    printf "This is a help message. This script can change SOFTWARE_UNDER_TEST
variable. You may find it useful while running specific test case
for various client/server implementations.\n
Usage: ./chsut
       --------  prints current SOFTWARE_UNDER_TEST variable
       ./chsut arg
       --------  changes SOFTWARE_UNDER_TEST to arg
       ./chsut -h
       --------  prints this message.\n\n"
elif [ $# -eq 0 ]; then
    grep "^SOFTWARE_UNDER_TEST*" $path/features/init_all.py
else
    printf "Changing SOFTWARE_UNDER_TEST variable to %s...\n" $1
    sed -i "s/^SOFTWARE_UNDER_TEST\ =\ \".*\",/SOFTWARE_UNDER_TEST\ =\ \"$1\",/" \
         $path/features/init_all.py
    printf "Done.\n"
fi
