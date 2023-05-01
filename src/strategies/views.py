import os
import shutil
import venv
import subprocess
from os import mkdir

from flask import Blueprint, jsonify, request
from datetime import datetime

from flask_login import current_user
from src import db
from src.strategies.models import Strategy

strategies_bp = Blueprint("strategies", __name__)

debug = True


@strategies_bp.route("/strategies/get_all", methods=["GET"])
def get_all_strategies():
    """Function used to fetch all strategies from the database"""
    strategies = Strategy.query.all()
    dictionaries = [strategy.as_dict() for strategy in strategies]
    response = jsonify(dictionaries)
    return response


@strategies_bp.route("/strategies/update", methods=["POST"])
def update_strategy():
    # Get the modified strategy
    request_strategy = request.json.get('strategy')

    try:
        # Find the strategy entry in the database
        strategy: Strategy = db.session.execute(
            db.select(Strategy).filter_by(id=request_strategy['id'])).scalar_one()
    except Exception as e:
        print(f"[ERROR] - [UPDATE STRATEGY QUERY]:\n{e}\n")
        response = jsonify(
            {'result': False, 'message': 'Strategy not found.', 'strategy': None})
        return response

    # Update the database entry
    strategy.name = request_strategy['name']
    strategy.description = request_strategy['description']
    strategy.input_type = request_strategy['input_type']
    strategy.output_type = request_strategy['output_type']
    strategy.stage = request_strategy['stage']
    strategy.last_modified_by = current_user.username
    strategy.updated_at = datetime.now()

    try:
        # Commiting will update the entry
        db.session.commit()
    except Exception as e:
        print(f"[ERROR] - [UPDATE STRATEGY COMMIT]:\n{e}\n")
        response = jsonify(
            {'result': False, 'message': 'Database error, could not commit.', 'strategy': None})
        return response

    response = jsonify(
        {'result': True, 'message': 'Strategy updated successfully.', 'strategy': strategy.as_dict()})
    return response


@strategies_bp.route("/strategies/delete", methods=["POST"])
def delete_strategy():
    # Get record id from the request
    strategy_id = request.json.get('id')

    # Find the strategy in the database
    try:
        strategy: Strategy = db.session.execute(
            db.select(Strategy).filter_by(id=strategy_id)).scalar_one()
    except Exception as e:
        print("[ERROR] - [STRATEGY DELETION]: ")
        print(e)
        response = jsonify(
            {'result': False, 'message': f'Error en la eliminación de la estategia.', 'strategy': None})
        return response

    try:
        strategy_dir = os.path.dirname(strategy.python_file_path)
        dir_deletion_result = delete_strategy_dir(strategy_dir)
        if not dir_deletion_result:
            response = jsonify(
                {'result': False, 'message': f'Error en la eliminación de la estategia.', 'strategy': None})
            return response
    except Exception as e:
        print("[ERROR] - [STRATEGY DELETION]: ")
        print(e)
        response = jsonify(
            {'result': False, 'message': f'Error en la eliminación de la estategia.', 'strategy': None})
        return response

    # Delete the strategy
    db.session.delete(strategy)
    db.session.commit()

    response = jsonify(
        {'result': True, 'message': f'Estrategia eliminada con éxito.', 'strategy': None})
    return response


@strategies_bp.route("/strategies/upload_python_file", methods=["POST"])
def save_python_file():
    py_file = request.files['file']
    file_path = request.form['python_file_path']
    try:
        py_file.save(file_path)
        response = jsonify(
            {'result': True, 'message': f'Guardado exitoso del fichero.'})
    except Exception as e:
        print(f"[ERROR] - [PYTHON FILE SAVING PROCESS]: {e}")
        error_message = 'No se pudo guardar el fichero correctamente'
        response = jsonify({'result': False, 'message': error_message})
    return response


@strategies_bp.route("/strategies/upload_requirements_file", methods=["POST"])
def save_requirements_file():
    requirements = request.files['file']
    strategy_dir = request.form['strategy_dir']
    try:
        requirements.save(strategy_dir + "requirements.txt")
        response = jsonify(
            {'result': True, 'message': f'Guardado exitoso del fichero.'})
    except Exception as e:
        print(f"[ERROR] - [PYTHON FILE SAVING PROCESS]: {e}")
        error_message = 'No se pudo guardar el fichero correctamente'
        response = jsonify({'result': False, 'message': error_message})
    return response


@strategies_bp.route("/strategies/create", methods=["POST"])
def create_strategy():
    strategy = build_strategy(request.json.get("strategy"))
    strategy_dir = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy.name}-strategy/'

    # Attempt to create and config virtual environment
    venv_creation_result = create_virtual_env(strategy)

    # Check venv creation result
    if venv_creation_result["result"] == False:
        if debug:
            print(
                "[DEBUG] - [VENV-CREATION-STDOUT]: Failed in the creation of the virtual environment.")
            print(strategy_dir)
        delete_strategy_dir(strategy_dir)
        response = jsonify(
            {'result': False, 'message': venv_creation_result["message"], 'strategy': strategy.as_dict()})
        return response

    # So far: strategy_dir and __init__.py created; py_file and requirements saved; venv created; all done!
    try:
        db.session.add(strategy)
        db.session.commit()
    except Exception as e:
        print(
            f"[ERROR] - [STRATEGY CREATION DATABASE ACCESS]: Strategy not properly deleted:\n{e}\n")

    response = jsonify(
        {'result': True, 'message': f'{strategy_dir}', 'strategy': strategy.as_dict()})
    return response


@strategies_bp.route("/strategies/setup_creation", methods=["POST"])
def setup_strategy_creation():
    strategy = build_strategy(request.json.get("strategy"))
    strategy_dir = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy.name}-strategy/'
    init_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy.name}-strategy/__init__.py'
    # Attempt to create stretegy_dir
    try:
        mkdir(strategy_dir)
        with open(init_path, "w") as file:
            pass
        if debug:
            print(
                "[DEBUG] - [VENV-CREATION-STDOUT]: Created strategy_dir and init file successfully!")
            print(strategy_dir)
        response = jsonify(
            {'result': True, 'message': f'{strategy_dir}', 'strategy': strategy.as_dict()})
    except Exception as e:
        print(f"[ERROR] - [STRATEGY DIR CREATION]: {e}")
        error_message = 'No se pudo crear el directorio, es posible que ya exista una estrategia con el mismo nombre'
        response = jsonify(
            {'result': False, 'message': error_message, 'strategy': strategy.as_dict()})
    return response


def build_strategy(strategy):
    strategy_name = strategy["name"]
    description = strategy["description"]
    input_type = strategy["input_type"]
    output_type = strategy["output_type"]
    stage = strategy["stage"]
    created_by = current_user.username
    last_modified_by = current_user.username
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type=input_type, output_type=output_type,
                        created_by=created_by, last_modified_by=last_modified_by, stage=stage)
    return strategy


def create_virtual_env(strategy):
    # Venv path
    env_dir = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy.name}-strategy/{strategy.name}-venv'
    # Requirements file
    requirements_file = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy.name}-strategy/requirements.txt'

    try:
        print("[DEBUG] - [VENV CREATION]: About to venv.create()")
        # Virtual environment creation
        venv.create(env_dir, with_pip=True)
    except Exception as e:
        print(f"[ERROR] - [ATTEMPTING VIRTUAL ENV CREATION]:\n{e}")
        return {'result': False, 'message': "Error during virtual environment creation"}

    try:
        print("[DEBUG] - [DEPENDENCY INSTALL]: About to subprocess.run")
        # Install dependencies
        subprocess.run([f"{env_dir}/bin/pip", "install",
                       "-r", requirements_file], check=True)
    except Exception as e:
        print(f"[ERROR] - [ATTEMPTING DEPENDENCY INSTALLATION]:\n{e}")
        return {'result': False, 'message': "Error during dependency installation"}

    return {'result': True, 'message': "Virtual environment created successfully!"}


def delete_strategy_dir(strategy_dir):
    if debug:
        print("\n[DEBUG] - [VENV-CREATION-STDOUT]: Deleting strategy_dir directory:")
        print(f"{strategy_dir}\n")
    try:
        shutil.rmtree(strategy_dir)
        return True
    except Exception as e:
        print(f"[ERROR] - [STRATEGY DIR DELETION]: {e}")
    return False
