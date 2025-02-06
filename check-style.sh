#!/bin/sh

# Usage:
# ./check-style.sh [--changed] [--bandit] [--pylint] [--pycodestyle] [--pydoctor] [--pydocstyle] [file, ...]

# shellcheck disable=SC2086
# SC2086 (info): Double quote to prevent globbing and word splitting.
# Reason: The unquoted files are files that need to be processed as separate words.

set -eu

script_path=$(cd "$(dirname "${0}")" && pwd)

files_to_search='forge src tests'
linters=''
while test ${#} -gt 0; do
  if test "${1-}" = '--changed'; then
    # Check only the files that were changed in this branch.
    files_to_search="$(git diff --name-only "$(git merge-base origin/master "$(git rev-parse --abbrev-ref HEAD)")")"
    shift
  elif echo "${1-}" | grep -E '^--'; then
    # Run linter.
    linter=$(echo "${1}" | sed 's/^--//')
    linters"${linters} ${linter}"
    shift
  else
    break
  fi
done

if test -z "${linters}"; then
  # If no linters were given, run all.
  linters='pylint pycodestyle pydoctor pydocstyle'
fi

cd "${script_path}"

if test ${#} -eq 0; then
  PY_FILES="$(find ${files_to_search} -name '*.py' -or -name 'forge' | sort -uV)"
  if test -z "${PY_FILES}"; then echo "No python scripts to check. Exiting early."; exit 0; fi
else
  # Check only the given files.
  PY_FILES="${*}"
fi

procs=$(grep -Fc proc < /proc/cpuinfo)

run_bandit() {
  bandit ${PY_FILES} || FAILURE=true
}

run_pylint() {
  pylint -j "${procs}" --rcfile=pylint.rc ${PY_FILES} || FAILURE=true
}

run_pycodestyle() {
  pycodestyle --max-line-length=3000 ${PY_FILES} || FAILURE=true
}

run_pydoctor() {
  pydoctor --docformat restructuredtext --html-output public . || FAILURE=true
}

run_pydocstyle() {
  pydocstyle ${PY_FILES} || FAILURE=true
}

# Call the linters.
printf 'Checking %s files...\n' "$(printf '%s\n' "${PY_FILES}" | wc -w)"
for linter in ${linters}; do
  printf '======== %s\n' "${linter}"
  "run_${linter}"
done

# This trick is so that all linters are run, while the script still exits
# with non-zero code if one of them fails.
if test -n "${FAILURE+x}"; then
  exit 1
fi
