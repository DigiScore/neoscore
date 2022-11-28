#!/bin/sh

set -e

echo "Running pre-commit cleanup"

# Disabled due to flaky behavior on some systems
# echo "Removing unused imports"
# unimport --check --remove --exclude "neoscore/common.py|.venv"

echo "Sorting imports"
isort .
echo "Formatting with black"
black .
