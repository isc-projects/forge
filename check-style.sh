#!/bin/bash

# Usage:
# ./check-style.sh
# `- Checks a predetermined list of python files.
#
# ./check-style.sh --all
# `- Checks all the files.
#
# ./check-style.sh --changed
# `- Checks only the files that were changed in this branch.
#
# ./check-style.sh file1.py file2.py ...
# `- Checks only the given files.

set -eu

script_path=$(cd "$(dirname "${0}")" && pwd)

if test "${1-}" = '--changed'; then
  files_to_search="$(git diff --name-only "$(git merge-base origin/master "$(git rev-parse --abbrev-ref HEAD)")")"
  shift
else
  files_to_search='.'
fi

cd "${script_path}"
if test ${#} -eq 0; then
    PY_FILES="$(find ${files_to_search} -name '*.py' | sort -uV)"
  else
    PY_FILES="${@}"
fi

printf 'Checking %s files...\n' "$(printf '%s\n' "${PY_FILES}" | wc -w)"
printf '======== pylint ========\n'
pylint -j "$(nproc || gnproc || echo 1)" --rcfile=pylint.rc ${PY_FILES}
printf '===== pycodestyle ======\n'
pycodestyle --max-line-length=3000 ${PY_FILES}
