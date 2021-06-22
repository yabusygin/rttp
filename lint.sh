#!/bin/sh

set -o errexit

exit_status_hook() {
    if [ $? -ne 0 ]; then
        echo "Failure"
    fi
}

trap exit_status_hook EXIT

PACKAGES="templtest tests"

echo "Running mypy..."
mypy $PACKAGES

echo "Running pylint..."
pylint $PACKAGES

echo "Running pycodestyle..."
pycodestyle $PACKAGES

echo "Running pydocstyle..."
pydocstyle $PACKAGES

echo "Success"
