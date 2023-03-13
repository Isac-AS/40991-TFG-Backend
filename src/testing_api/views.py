import pickle
import subprocess
from flask import Blueprint, jsonify, request
from datetime import datetime

from src import db
from flask_login import current_user
from src.pipelines.models import Pipeline
from src.strategies.models import Strategy
from src.health_records.models import HealthRecord

testing_bp = Blueprint("testing", __name__)


@testing_bp.route("/api/test", methods=["GET", "POST"])
def random_testing():
    strategy_input = "Posible texto en español con faltas de ortografia como no ponel tildes y demas"
    strategy: Strategy = db.session.execute(
        db.select(Strategy).filter_by(id=2)).scalar_one()
    process = subprocess.Popen([strategy.env_path, strategy.python_file_path,
                               strategy_input], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    # Get the output
    serialized_output = stdout.strip()
    print(f'\nStdout:\n{stdout}\n\nSerialized output:\n{serialized_output}\n')
    strategy_output = pickle.loads(serialized_output)
    print(f'Strategy output: {strategy_output}')

    diccionario = {'output': 'la verdad es que este es un diccionario de prueba'}
    diccionario_serializado = pickle.dumps(diccionario)
    print(f'Diccionario:\n{diccionario}\nDiccionario serializado:\n{diccionario_serializado}')
    diccionario_deserializado = pickle.loads(diccionario_serializado)
    print(f'Diccionario deserializado:\n{diccionario_deserializado}')

    return jsonify({"ping": "pong!"})


@testing_bp.route("/api/test/audio_saving", methods=["GET", "POST"])
def attempt_audio_save():
    audio = request.files['audio']
    audio.save(
        f"/opt/40991-TFG-Backend/recordings/{current_user.username}-{audio.filename}")
    print(audio)

    # print(request.json)
    # print(request.json.get("audio"))
    return jsonify({"ping": "pong!"})


@testing_bp.route("/api/test/reset_database", methods=["GET", "POST"])
def reset_database():
    # db.drop_all()
    # db.create_all()
    return jsonify({"ping": "pong!"})


@testing_bp.route("/api/test/add_strategy", methods=["GET", "POST"])
def add_strategy():
    """strategy_name = "pyspellchecker"
    description = "Estrategia empleada para corregir posibles errores ortográficos de la transcripción"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Intermedia")"""
    """strategy_name = "sample_adt_a01"
    description = "Estrategia de ejemplo para crear una historia clínica electrónica"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Final")"""
    """strategy_name = "whisper"
    description = "Estrategia de conversión de voz a texto usando la herramienta 'whisper' de openai"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Voz a texto")"""
    """db.session.add(strategy)
    db.session.commit()"""
    return jsonify({"ping": "pong!"})


@testing_bp.route("/api/test/add_pipeline", methods=["GET", "POST"])
def add_pipeline():
    # db.drop_all()
    # db.create_all()
    return jsonify({"ping": "pong!"})


@testing_bp.route("/api/test/add_record", methods=["GET", "POST"])
def add_health_record():
    # db.drop_all()
    # db.create_all()
    return jsonify({"ping": "pong!"})


def pipeline_testing():
    pipeline = Pipeline(
        name='Test-Pipeline 1',
        description='Pipline to test if the table will display the array',
        strategies=[
            {'id': '1', 'name': 'test_name1'},
            {'id': '2', 'name': 'test_name2'},
            {'id': '3', 'name': 'test_name3'}
        ],
        created_by='Testing',
        last_modified_by='Testing'
    )
    db.session.add(pipeline)
    db.session.commit()
    return None


def run_subprocess():
    # env = {'PATH': './strategies_implementations/whisper-venv/bin'}
    strategy_name = "whisper"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    recording_filename = "recording.wav"
    recording_path = f"/opt/40991-TFG-Backend/recordings/{recording_filename}"
    arg1 = recording_path
    # serialized_data = pickle.dumps(arg1)
    # process = subprocess.Popen(['/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper.py', arg1], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
