#!/bin/sh

set -e

echo "Running pre-commit cleanup"

echo "Removing unused imports"
unimport --check --remove --exclude "neoscore/common.py|.venv"

echo "Sorting imports"
isort .
echo "Formatting with black"
black .
