#!/bin/bash

set -eu

script_path=$(cd "$(dirname "${0}")" && pwd)

cd "${script_path}"
if [ $# -eq 0 ]
  then
    PY_FILES="$(find tests/{dhcpv4,dhcpv6,other_tests,HA,iscdhcp}/ -name '*.py' | sort -V)"
  else
    PY_FILES="$@"
fi

printf 'Checking %s files...\n' "$(printf '%s\n' "${PY_FILES}" | wc -w)"

pylint -j "$(nproc || gnproc || echo 1)" --rcfile=pylint.rc --disable=C0209 ${PY_FILES}
pycodestyle --max-line-length=3000 ${PY_FILES}
