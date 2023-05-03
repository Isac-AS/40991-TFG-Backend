#!/bin/bash
export FLASK_APP=./src/
source .test_env
python -m pytest
# Remove comment below to verbose the fixture execution in relation to the tests.
#python -m pytest --setup-show

