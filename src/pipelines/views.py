from flask import Blueprint, jsonify, request
from datetime import datetime
from src import db
from src.pipelines.models import Pipeline

pipelines_bp = Blueprint("pipelines", __name__)

@pipelines_bp.route("/pipelines/get_all", methods=["GET"])
def get_all_pipelines():
    """Function used to fetch all pipelines from the database"""
    pipelines = Pipeline.query.all()
    dictionaries = [pipeline.as_dict() for pipeline in pipelines]
    response = jsonify(dictionaries)
    return response

@pipelines_bp.route("/pipelines/read", methods=["POST"])
def get_pipeline():
    pass

@pipelines_bp.route("/pipelines/create", methods=["POST"])
def create_pipeline():
    pass

@pipelines_bp.route("/pipelines/update", methods=["POST"])
def update_pipeline():
    pass

@pipelines_bp.route("/pipelines/delete", methods=["POST"])
def delete_pipeline():
    # Get pipeline id from the response
    pipeline_id = request.json.get('id')
    # Find the pipeline in the database
    pipeline: Pipeline = db.session.execute(db.select(Pipeline).filter_by(id = pipeline_id )).scalar_one()
    # Delete the pipeline
    db.session.delete(pipeline)
    db.session.commit()

    response = jsonify({'result': True, 'message': f'Pipeline "{pipeline.name}" eliminado con éxito.', 'pipeline': None})
    return response
