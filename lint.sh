#!/bin/sh

# Usage:
# ./lint.sh [--add-init.py] [--changed] [--bandit] [--pylint] [--pycodestyle] [--pydoctor] [--pydocstyle] [file, ...]

# shellcheck disable=SC2086
# SC2086 (info): Double quote to prevent globbing and word splitting.
# Reason: The unquoted files are files that need to be processed as separate words.

set -eu

script_path=$(cd "$(dirname "${0}")" && pwd)

# Adds __init.py__ files to all directories that are missing __init__.py files.
add_init_py() {
  find . -type d \
    -not -path './.git*' \
    -exec test ! -f '{}/__init__.py' ';' \
    -exec touch '{}/__init__.py' ';' \
    -exec echo '{}/__init__.py' ';'
}

files_to_search='forge src tests'
linters=''
while test ${#} -gt 0; do
  if test "${1-}" = '--add-init.py'; then
    add_init_py
    exit 0
  elif test "${1-}" = '--changed'; then
    # Check only the files that were changed in this branch.
    files_to_search="$(git diff --name-only "$(git merge-base origin/master "$(git rev-parse --abbrev-ref HEAD)")")"
    shift
  elif echo "${1-}" | grep -E '^--'; then
    # Run linter.
    linter=$(echo "${1}" | sed 's/^--//')
    linters="${linters} ${linter}"
    shift
  else
    break
  fi
done

if test -z "${linters}"; then
  # If no linters were given, run all.
  linters='bandit pycodestyle pydocstyle pydoctor pylint'
fi

cd "${script_path}"

if test ${#} -eq 0; then
  PY_FILES="$(find ${files_to_search} -name '*.py' -or -name 'forge' | sort -uV)"
  if test -z "${PY_FILES}"; then echo "No python scripts to check. Exiting early."; exit 0; fi
else
  # Check only the given files.
  PY_FILES="${*}"
fi

if [ -f /proc/cpuinfo ]; then
    procs=$(grep -Fc proc < /proc/cpuinfo)
else
    procs=4
fi

run_bandit() {
  bandit -c bandit.yaml ${PY_FILES} || FAILURE=true
}

run_pylint() {
  pylint -j "${procs}" --rcfile=pylint.rc ${PY_FILES} || FAILURE=true
}

run_pycodestyle() {
  pycodestyle --max-line-length=3000 ${PY_FILES} || FAILURE=true
}

run_pydoctor() {
  # __init__.py files are required by pydoctor.
  files=$(add_init_py)
  pydoctor --docformat restructuredtext --testing . || FAILURE=true
  echo  # pydoctor does not add a trailing new line. Add it ourselves.
  rm ${files}
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
