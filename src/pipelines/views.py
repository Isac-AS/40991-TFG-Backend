import subprocess
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

@pipelines_bp.route("/pipelines/run_pipeline", methods=["POST"])
def run_pipeline():
    return

# Example subprocess run
def run_strategy(strategy_input, strategy_name):
    # Subprocess 
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    #serialized_data = pickle.dumps(arg1)
    #process = subprocess.Popen(['/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper.py', arg1], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen([
        env_path,
        file_path,
        arg1],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Esperar a que el proceso termine
    stdout, stderr = process.communicate()
    # Imprimir la salida del programa
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    return None
