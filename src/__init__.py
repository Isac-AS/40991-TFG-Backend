import pickle
import subprocess
import os
import sys
import importlib.util

from decouple import config
from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf

# create flask application
app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
app.secret_key = 'soadbausodboas'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)
cors = CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Registering blueprints
from src.accounts.views import accounts_bp
app.register_blueprint(accounts_bp)

from src.health_records.views import health_record_bp
app.register_blueprint(health_record_bp)

from src.pipelines.views import pipelines_bp
app.register_blueprint(pipelines_bp)

from src.strategies.views import strategies_bp
app.register_blueprint(strategies_bp)

# Definition of load_user callback
from src.accounts.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

# Common api methods
@app.route("/api/ping", methods=["GET", "POST"])
def home():
    return jsonify({"ping": "pong!"})

@app.route("/api/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response


def run_subprocess():
    env = {'PATH': './strategies_implementations/whisper-venv/bin'}
    
    file_path = '/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper.py'
    arg1 = '../recordings/test_recording_0.wav'
    serialized_data = pickle.dumps(arg1)
    #process = subprocess.Popen(['/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper.py', arg1], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen([
        '/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper-venv/bin/python',
        '/opt/40991-TFG-Isac/backend/src/strategies_implementations/whisper/whisper.py',
        arg1],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Esperar a que el proceso termine
    stdout, stderr = process.communicate()
    # Imprimir la salida del programa
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    return None



# Testing area 
from src.pipelines.models import Pipeline
from src.pipelines.views import get_all_pipelines
@app.route("/api/test", methods=["GET", "POST"])
def random_testing():
    #db.create_all()
    #pipeline_testing()
    run_subprocess()
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