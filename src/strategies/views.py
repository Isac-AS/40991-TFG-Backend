from flask import Blueprint, jsonify, request
from datetime import datetime

from flask_login import current_user
from src import db
from src.strategies.models import Strategy

strategies_bp = Blueprint("strategies", __name__)


@strategies_bp.route("/strategies/get_all", methods=["GET"])
def get_all_strategies():
    """Function used to fetch all strategies from the database"""
    strategies = Strategy.query.all()
    dictionaries = [strategy.as_dict() for strategy in strategies]
    response = jsonify(dictionaries)
    return response


@strategies_bp.route("/strategies/read", methods=["POST"])
def get_strategy():
    pass


@strategies_bp.route("/strategies/create", methods=["POST"])
def create_strategy():
    strategy_name = request.json.get("name")
    description = request.json.get("description")
    input_type = request.json.get("input_type")
    output_type = request.json.get("output_type")
    stage = request.json.get("stage")
    created_by = current_user.username
    last_modified_by = current_user.username
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type=input_type, output_type=output_type,
                        created_by=created_by, last_modified_by=last_modified_by, stage=stage)
    db.session.add(strategy)
    db.session.commit()
    return


@strategies_bp.route("/strategies/update", methods=["POST"])
def update_strategy():
    pass


@strategies_bp.route("/strategies/delete", methods=["POST"])
def delete_strategy():
    pass
