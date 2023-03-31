import json
import os
import pickle
import subprocess
import sys
import traceback
from flask import Blueprint, jsonify, request
from datetime import datetime

from flask_login import current_user
from src import db
from src.health_records.models import HealthRecord
from src.pipelines.models import Pipeline
from src.strategies.models import Strategy

health_record_bp = Blueprint("health_records", __name__)

debug = True


@health_record_bp.route("/health_records/get_all", methods=["GET"])
def get_all_health_records():
    """Function used to fetch all health records from the database"""
    health_records = HealthRecord.query.all()
    dictionaries = [record.as_dict() for record in health_records]
    response = jsonify(dictionaries)
    return response


@health_record_bp.route("/health_records/save_audio", methods=["POST"])
def save_audio():
    audio = request.files['audio']
    audio_file_path = f"/opt/40991-TFG-Backend/recordings/{current_user.username}_{audio.filename}"
    audio.save(audio_file_path)
    return jsonify({'result': True, 'message': "Audio guardado correctamente", "audio_file_path": audio_file_path})


@health_record_bp.route("/health_records/delete", methods=["POST"])
def delete_health_record():
    # Get record id from the request
    record_id = request.json.get('id')
    # Find the pipeline in the database
    record: HealthRecord = db.session.execute(
        db.select(HealthRecord).filter_by(id=record_id)).scalar_one()
    # Delete the recording if it is a parent record
    if record.parent_id is None:
        os.remove(record.recording_path)
    # Delete the pipeline
    db.session.delete(record)
    db.session.commit()

    response = jsonify(
        {'result': True, 'message': f'Pipeline "{record.id}" eliminado con éxito.', 'pipeline': None})
    return response


@health_record_bp.route("/health_records/read", methods=["POST"])
def get_health_record():
    pass


@health_record_bp.route("/health_records/update", methods=["POST"])
def update_health_record():
    pass


@health_record_bp.route("/health_records/create_from_audio", methods=["POST"])
def create_health_record_from_audio():
    """API method to add a new electronic health record to the database.

    The record is new and an audio file will be received from the 
    frontend, and it will be stored and used as the first input of the
    pipeline.

    :param pipeline_id: Unique identifier of the pipeline to be run
    :type pipeline_id: int
    :param audio_file_path: Path to audio file
    :type audio_file_path: string
    :return: Standard response
    :rtype: http_response
    """
    # Request information extraction
    pipeline_id = request.json.get("pipeline_id")
    audio_file_path = request.json.get("audio_file_path")

    # Run the pipeline to create the record
    pipeline_output = run_pipeline(
        pipeline_id=pipeline_id, skip_steps=0, strategy_input=audio_file_path)

    # Create the record object. As it is a new record from audio, it is assumed
    # that the first output is the transcription and the last output the EHR.
    new_record = HealthRecord(
        recording_path=audio_file_path,
        transcription=pipeline_output[0]['strategy_output']['output'],
        health_record=pipeline_output[-1]['strategy_output']['output'],
        processing_outputs=pipeline_output,
        parent_id=None,
        created_by=current_user.username,
        last_modified_by=current_user.username
    )

    try:
        db.session.add(new_record)
        db.session.commit()
    except:
        print(traceback.print_exc())
        print("\nPipeline output:")
        print(pipeline_output)
        print(json.dumps(pipeline_output))
        return jsonify(
            {'result': False, 'message': '¡Error durante el acceso a la base de datos!', 'healthRecord': None})

    response = jsonify(
        {'result': True, 'message': '¡Registro creado con éxito!', 'healthRecord': new_record.as_dict()})
    return response


@health_record_bp.route("/health_records/create_from_record", methods=["POST"])
def create_health_record_from_record():
    """API method to add a new electronic health record to the database.

    The record is created using data from a previous record, a
    new record will be added using the data from its parent and the 
    pipeline provided.

    :param pipeline_id: Unique identifier of the pipeline to be run
    :type pipeline_id: int
    :param record_id: Potential parent record identifier
    :type record_id: int | None
    :param skip_steps: Steps of the pipeline should be skipped and how many
    :type skip_steps: int
    :return: Standard response
    :rtype: http_response
    """
    parent_health_record_id = request.json.get("parent_health_record_id")
    parent_health_record_recording_path = request.json.get(
        "parent_health_record_recording_path")
    parent_health_record_transcription = request.json.get(
        "parent_health_record_transcription")
    skip_steps = request.json.get("skip_steps")
    strategy_input = request.json.get("strategy_input")
    pipeline_id = request.json.get("pipeline_id")

    pipeline_output = run_pipeline(
        pipeline_id=pipeline_id, skip_steps=skip_steps, strategy_input=strategy_input)

    new_record = HealthRecord(
        recording_path=parent_health_record_recording_path,
        transcription=parent_health_record_transcription,
        health_record=pipeline_output[-1]['strategy_output']['output'],
        processing_outputs=pipeline_output,
        parent_id=parent_health_record_id,
        created_by=current_user.username,
        last_modified_by=current_user.username
    )

    try:
        db.session.add(new_record)
        db.session.commit()
    except:
        print(traceback.print_exc())
        print("\nPipeline output:")
        print(pipeline_output)
        print(json.dumps(pipeline_output))
        return jsonify(
            {'result': False, 'message': '¡Error durante el acceso a la base de datos!', 'healthRecord': None})

    response = jsonify(
        {'result': True, 'message': '¡Registro creado con éxito!', 'healthRecord': new_record.as_dict()})
    return response


def run_pipeline(pipeline_id, skip_steps, strategy_input):
    """Will run a stored pipeline from the database

    :param pipeline_id: Unique id of the pipeline
    :type pipeline_id: int
    :param skip_steps: Whether certain steps of the pipeline should be skipped and how many
    :type skip_steps: int
    :param strategy_input: Input for the first strategy
    :type strategy_input: string
    :return: Dictionary with the strategy name and output
    :rtype: dict
    """
    # Find the pipeline in the database
    pipeline: Pipeline = db.session.execute(
        db.select(Pipeline).filter_by(id=pipeline_id)).scalar_one()
    # Step skipping
    strategies_to_run = pipeline.strategies[skip_steps:]
    print(f"[DEBUG] - Strategies to run: {strategies_to_run}")
    # Get first input
    pipeline_output = []
    for strategy in strategies_to_run:
        # Run strategy
        strategy_output = run_strategy(
            strategy_input=strategy_input, strategy_id=strategy["id"])

        # Build output dict
        current_output = {
            'strategy_id': strategy["id"],
            'strategy_name': strategy["name"],
            'strategy_output': strategy_output,
        }
        # Add output dict to the pipeline output
        pipeline_output.append(current_output)

        # Prepare current output as next input
        strategy_input = strategy_output['output']
    return pipeline_output


def run_strategy(strategy_input, strategy_id):
    """Will run a single strategy as a subprocess and return the output

    :param strategy_input: Input data to the strategy
    :type strategy_input: any | string
    :param strategy_id: Unique identifier of the strategy
    :type strategy_id: int
    :return: Output of the strategy
    :rtype: any
    """
    # Get strategy information from the database
    strategy: Strategy = db.session.execute(
        db.select(Strategy).filter_by(id=strategy_id)).scalar_one()

    # Run strategy as subprocess
    # As JSON will be used to pass dictionary objects, the text_mode of the underlying object is true.
    process = subprocess.Popen([strategy.env_path, strategy.python_file_path],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Prepare the strategy input
    strategy_input_dict = {'input': strategy_input}
    serialized_input_dict = json.dumps(strategy_input_dict)

    # Wait for the process to finish
    stdout, stderr = process.communicate(input=serialized_input_dict)

    try:
        strategy_output = json.loads(stdout)
    except Exception:
        print(
            f"\n\n[ERROR] - Couldn't load output of the strategy: '{strategy.as_dict()['name']}'")
        print(f"[ERROR] - Traceback:")
        print(traceback.print_exc())
        print(f"\n[ERROR] - Stderr:\n{stderr}")
        strategy_output = {'output': 'Error durante esta estrategia'}

    # Print debugging info
    if debug:
        print(f"\n\n\n[DEBUG] - Current strategy:\n{strategy.as_dict()}")
        print(f"\n[DEBUG] - Strategy input:\n{strategy_input}")
        print(f"\n[DEBUG] - Stdout:\n{stdout}")
        # print(f"\n[DEBUG] - Serialized output:\n{serialized_output}")
        print(f"\n[DEBUG] - Strategy output:\n{strategy_output}")
    return strategy_output
