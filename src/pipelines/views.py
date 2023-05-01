import pickle
import subprocess
from flask import Blueprint, jsonify, request
from datetime import datetime

from flask_login import current_user
from src import db
from src.pipelines.models import Pipeline

pipelines_bp = Blueprint("pipelines", __name__)

debug = True


@pipelines_bp.route("/pipelines/get_all", methods=["GET"])
def get_all_pipelines():
    """Function used to fetch all pipelines from the database"""
    pipelines = Pipeline.query.all()
    dictionaries = [pipeline.as_dict() for pipeline in pipelines]
    response = jsonify(dictionaries)
    return response


@pipelines_bp.route("/pipelines/create", methods=["POST"])
def create_pipeline():

    # Get info from request
    incoming_pipeline = request.json.get("pipeline")
    name = incoming_pipeline["name"]
    description = incoming_pipeline["description"]
    strategies = incoming_pipeline["strategies"]

    # Look for pipeline with the same name
    result = db.session.execute(
        db.select(Pipeline).where(Pipeline.name == name))

    if len(result.all()) > 0:
        response = jsonify(
            {'result': False, 'message': 'Ya existe un pipeline con ese nombre.', 'pipeline': None})
        return response

    new_pipeline = Pipeline(
        name=name,
        description=description,
        strategies=strategies,
        created_by=current_user.username,
        last_modified_by=current_user.username)

    db.session.add(new_pipeline)
    db.session.commit()

    response = jsonify(
        {'result': True, 'message': '¡Pipeline creado con éxito!', 'pipeline': new_pipeline.as_dict()})
    return response


@pipelines_bp.route("/pipelines/update", methods=["POST"])
def update_pipeline():
    # Get the modified pipeline
    request_pipeline = request.json.get('pipeline')

    try:
        # Find the pipeline entry in the database
        pipeline: Pipeline = db.session.execute(
            db.select(Pipeline).filter_by(id=request_pipeline['id'])).scalar_one()
    except Exception as e:
        print(f"[ERROR] - [UPDATE PIPELINE QUERY]:\n{e}\n")
        response = jsonify(
            {'result': False, 'message': 'Pipeline not found.', 'pipeline': None})
        return response

    # Update the database entry
    pipeline.name = request_pipeline['name']
    pipeline.description = request_pipeline['description']
    pipeline.last_modified_by = current_user.username
    pipeline.updated_at = datetime.now()

    try:
        # Commiting will update the entry
        db.session.commit()
    except Exception as e:
        print(f"[ERROR] - [UPDATE PIPELINE COMMIT]:\n{e}\n")
        response = jsonify(
            {'result': False, 'message': 'Database error, could not commit.', 'pipeline': None})
        return response

    response = jsonify(
        {'result': True, 'message': 'Pipeline updated successfully.', 'pipeline': pipeline.as_dict()})
    return response


@pipelines_bp.route("/pipelines/delete", methods=["POST"])
def delete_pipeline():
    # Get pipeline id from the request
    pipeline_id = request.json.get('id')
    # Find the pipeline in the database
    pipeline: Pipeline = db.session.execute(
        db.select(Pipeline).filter_by(id=pipeline_id)).scalar_one()
    # Delete the pipeline
    db.session.delete(pipeline)
    db.session.commit()

    response = jsonify(
        {'result': True, 'message': f'Pipeline "{pipeline.name}" eliminado con éxito.', 'pipeline': None})
    return response
