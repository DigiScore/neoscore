#!/bin/sh

# Ensure certain slow imports are not used

# Disallow importing PyQt5.Qt This adds >30ms to startup times because
# it's such a big module which pulls in many other Qt modules. It
# seems to not be generally needed though, since it's mostly
# (entirely?) used for enum declarations which can be substituted with
# integer values. This rule can be revisited later if necessary.
if grep -E -r 'from PyQt5 import Qt\b|from PyQt5.Qt import\b|from PyQt5 import .*\bQt\b' neoscore
then
    echo "Imports of PyQt5.Qt are not allowed, as it is very slow. Directly use enum int values instead."
    exit 1
fi
