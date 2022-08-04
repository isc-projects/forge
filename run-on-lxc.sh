#!/bin/sh

# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Exit with error if commands exit with non-zero and if undefined variables are
# used.
set -eu

# Print usage.
print_usage() {
  printf \
'Usage: %s {{options}}
Options:
  [-d|--debug]                      enable debug mode, showing every executed command
  [-h|--help]                       print usage (this text)
  -c|--ccache-dir ${ccache_dir}     ccache directory
  -k|--kea-dirs ${kea_dirs}         Kea directories
  [-i|--install-kea]                whether to install-kea or not
  -l|--label ${label}               label included in XML name and in the name of the tarball containing the results
  -m|--mark ${mark}                 cb | ddns | ha | v4 | v6
  [-p|--pytest-args ${pytest_args}] any additional arguments to pass to pytest
  -s|--system ${system}             system e.g. `debian-11`
Example:
  ./run-on-lxc.sh -c /tmp/ccache-dir -k /tmp/kea-dirs -i -l label -m v4 -p "-m v4" -s fedora-36
' \
    "$(basename "${0}")"
}

# Parse parameters.
while test ${#} -gt 0; do
  case "${1}" in
    '-d'|'--debug') set -vx ;;
    '-h'|'--help') print_usage; exit 0 ;;
    '-c'|'--ccache-dir') shift; ccache_dir=${1} ;;
    '-k'|'--kea-dirs') shift; kea_dirs=${1} ;;
    '-i'|'--install-kea') install_kea=true ;;
    '-l'|'--label') shift; label=${1} ;;
    '-m'|'--mark') shift; mark=${1} ;;
    '-p'|'--pytest-args') shift; pytest_args=${1} ;;
    '-s'|'--system') shift; system=${1} ;;

    # Unrecognized argument
    *) printf "${red}ERROR: Unrecognized argument '%s'${reset}\\n" "${1}" 1>&2; print_usage; exit 1 ;;
  esac; shift
done

# Default parameters
test -z "${install_kea}" && install_kea=false

# Switch to the same directory as the script.
cd "$(dirname "${0}")"

mkdir -p "${ccache_dir}"
mkdir -p "${kea_dirs}"

rm -rf venv
python3 -m venv venv
venv/bin/pip install -U pip
venv/bin/pip install -r ./requirements.txt
venv/bin/python ./forge config ccache-dir "${ccache_dir}"
venv/bin/python ./forge config kea-dirs "${kea_dirs}"
if test -f "vagrant/lxc/${mark}/${system}/Vagrantfile"; then
  venv/bin/python ./forge --lxc --sid "${mark}" -s "${system}" clean
fi
venv/bin/python ./forge --lxc --sid "${mark}" -s "${system}" setup
if "${install_kea}"; then
  venv/bin/python ./forge --lxc --sid "${mark}" -s "${system}" install-kea kea
fi
venv/bin/python ./forge --lxc --sid "${mark}" -s "${system}" test -r ap -vv --junitxml "kea-${label}.xml" ${pytest_args} || true
tar -pczf "forge-${label}.tar.gz" tests_results
venv/bin/python ./forge --lxc --sid "${mark}" -s "${system}" terminate-instances
