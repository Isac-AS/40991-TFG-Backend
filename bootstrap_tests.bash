#!/bin/bash
export FLASK_APP=./src/
source .test_env
python -m pytest --setup-show tests/unit/
#python -m pytest

