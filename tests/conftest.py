import os
import pytest
from src import app as flask_app
from src import db
from src.accounts.models import User
from src.pipelines.models import Pipeline
from flask_login import login_user


@pytest.fixture()
def app():
    app = flask_app
    # Setup can go here
    with flask_app.app_context():
        # Create all database models
        db.create_all()

    yield app

    # clean up / reset resources here
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
        # testdb_path = "/opt/40991-TFG-Backend/instance/testdb.sqlite"
        # os.remove(testdb_path)


@pytest.fixture()
def client(app):
    return flask_app.test_client()

@pytest.fixture()
def database(app):
    return db

@pytest.fixture()
def register(client):
    with flask_app.app_context():
        client.post("/register", json={
            "username": "test_user",
            "email": "test@user.com",
            "role": 1,
            "password": "test_user"
        })
