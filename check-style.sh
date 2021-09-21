#!/bin/bash
set -e -x

PY_FILES=`find tests/{dhcpv4,dhcpv6,other_tests,HA}/ -name '*.py'`
time pylint -j $(expr \( `nproc` + 1 \) / 2) --rcfile=pylint.rc --disable=C0209 $PY_FILES
pycodestyle --max-line-length=3000 --ignore=E722 $PY_FILES
