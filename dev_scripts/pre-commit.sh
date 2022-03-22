#!/bin/sh

echo "Running pre-commit cleanup"

set -e

echo "Formatting with black"
black .
echo "Removing unused imports"
# Note that this returns exit code 1 when imports are fixed
# so need to disable error bailing here
set +e
unimport --check --remove --exclude neoscore/common.py
set -e
echo "Sorting imports"
isort .
