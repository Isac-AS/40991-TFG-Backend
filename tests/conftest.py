import pytest
from src import app as flask_app
from src import db
from src.accounts.models import User
from src.pipelines.models import Pipeline
from flask_login import login_user


@pytest.fixture()
def app():
    app = flask_app.config.from_object("config.TestingConfig")

    # Setup can go here
    with flask_app.app_context():
        # Create all database models
        db.create_all()
        # Create a user
        example_user = User(
            username="test_admin",
            password="admin_user",
            email="ad@min.com",
            role=10,
            created_by="cli",
            last_modified_by="cli",
            is_admin=True,
        )
        db.session.add(example_user)
        db.session.commit()

    yield app

    # clean up / reset resources here
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
    # testdb_path = "/opt/40991-TFG-Backend/instance/testdb.sqlite"


@pytest.fixture()
def client(app):
    return flask_app.test_client()


@pytest.fixture(scope="function")
def login(app):
    with flask_app.app_context():
        email = "ad@min.com"
        user: User = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        login_user(user)


@pytest.fixture(scope="module")
def test_pipeline():
    pipeline = Pipeline(
        name="test_pipeline",
        description="test_pipeline_description",
        strategies=[],
        created_by="test",
        last_modified_by="test"
    )
    return pipeline
