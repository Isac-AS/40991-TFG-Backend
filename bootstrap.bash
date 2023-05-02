#!/bin/bash
export FLASK_APP=./src/
source .env
source ./venv/bin/activate
flask run -h 0.0.0.0

