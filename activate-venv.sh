#!/bin/sh

# This script needs to be sourced to work.
# . ./activate-venv.sh

if test ! -d ./venv; then
  printf 'Creating venv...\n'
  python3 -m venv ./venv
  ./venv/bin/pip install --upgrade pip
  ./venv/bin/pip install -r requirements.txt
fi

. ./venv/bin/activate
