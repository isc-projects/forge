#!/bin/sh

# This script needs to be sourced to work.
# . ./activate-venv.sh

if test ! -d ./venv; then
  printf 'Creating venv...\n'
  python3 -m venv ./venv
  ./venv/bin/pip install --upgrade pip
  ./venv/bin/pip install -r requirements.txt
  ./venv/bin/pip install pylint==2.15.5 pycodestyle==2.9.0
fi

. ./venv/bin/activate
