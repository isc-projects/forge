#!/bin/sh

# Usage:
# ./check-style.sh
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
  files_to_search='forge src tests'
fi

cd "${script_path}"

if test ${#} -eq 0; then
  PY_FILES="$(find ${files_to_search} -name '*.py' -or -name 'forge' | sort -uV)"
else
  PY_FILES="${@}"
fi

printf 'Checking %s files...\n' "$(printf '%s\n' "${PY_FILES}" | wc -w)"
printf '======== pylint ========\n'
pylint   --rcfile=pylint.rc ${PY_FILES} || pylint_failed=true
printf '===== pycodestyle ======\n'
pycodestyle --max-line-length=3000 ${PY_FILES}

# This trick is so that both linters are run, while the script still exits
# with non-zero code if one of them fails.
if test -n "${pylint_failed+x}"; then
  exit 1
fi
