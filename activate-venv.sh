#!/bin/bash

# This script needs to be sourced to work.
# . ./activate-venv.sh

if test ! -d ./venv; then
  printf 'Creating venv...\n'
  python3 -m venv ./venv
  ./venv/bin/pip install --upgrade pip
  ./venv/bin/pip install -r requirements.txt
  ./venv/bin/pip install pylint==3.0.3 pycodestyle==2.11.1
fi

. ./venv/bin/activate
