from flask import Blueprint, jsonify, request
from datetime import datetime
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
    pass

@strategies_bp.route("/strategies/update", methods=["POST"])
def update_strategy():
    pass

@strategies_bp.route("/strategies/delete", methods=["POST"])
def delete_strategy():
    pass
