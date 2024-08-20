#!/usr/bin/env bash
# set -eux

export PIP_REQUIRE_VIRTUALENV=false

pip3 install virtualenv
virtualenv venv
source ./venv/bin/activate
pip3 install pytest
pytest
