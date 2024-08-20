#!/usr/bin/env bash
# set -eux

export PIP_REQUIRE_VIRTUALENV=false

pip3 install virtualenv
virtualenv venv
source ./venv/bin/activate
pip3 install black ruff

# Run black
echo -e "Running black test"
black .

# Check linting
echo -e "Performing ruff linting tests\n"
ruff check --fix .
