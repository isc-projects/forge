#!/bin/bash
set -e -x

pushd lettuce
PY_FILES=`find features/{dhcpv4,dhcpv6,other_tests}/ -name '*.py'`
PY_FILES="$PY_FILES feat2py.py"
pylint --rcfile=../pylint.rc $PY_FILES
pycodestyle --max-line-length=2000 --ignore=E722 $PY_FILES
