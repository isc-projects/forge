#!/bin/bash
set -e -x

PY_FILES=`find tests/{dhcpv4,dhcpv6,other_tests}/ -name '*.py'`
PY_FILES="$PY_FILES feat2py.py"
time pylint -j $(expr \( `nproc` + 1 \) / 2) --rcfile=pylint.rc $PY_FILES
pycodestyle --max-line-length=2000 --ignore=E722 $PY_FILES
