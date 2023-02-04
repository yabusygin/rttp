#!/bin/sh

set -o errexit

exit_status_hook() {
    if [ $? -ne 0 ]; then
        echo "Failure"
    fi
}

trap exit_status_hook EXIT

PACKAGES="templtest tests"

echo "Running black..."
black --check $PACKAGES

echo "Running mypy..."
mypy --non-interactive $PACKAGES

echo "Running pylint..."
pylint --redefining-builtins-modules=sys $PACKAGES

echo "Running pydocstyle..."
pydocstyle $PACKAGES

echo "Success"
