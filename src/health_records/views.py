from flask import Blueprint, jsonify, request
from datetime import datetime
from src import db
from src.health_records.models import HealthRecord

health_record_bp = Blueprint("health_records", __name__)

@health_record_bp.route("/health_records/get_all", methods=["GET"])
def get_all_health_records():
    """Function used to fetch all health records from the database"""
    health_records = HealthRecord.query.all()
    dictionaries = [record.as_dict() for record in health_records]
    response = jsonify(dictionaries)
    return response

@health_record_bp.route("/health_records/read", methods=["POST"])
def get_health_record():
    pass

@health_record_bp.route("/health_records/create", methods=["POST"])
def create_health_record():
    pass

@health_record_bp.route("/health_records/update", methods=["POST"])
def update_health_record():
    pass

@health_record_bp.route("/health_records/delete", methods=["POST"])
def delete_health_record():
    pass
