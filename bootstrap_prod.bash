#!/bin/bash
export FLASK_APP=./src/
source .env_prod
source ./venv/bin/activate
flask run -h 0.0.0.0

