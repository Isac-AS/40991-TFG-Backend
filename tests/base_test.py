import os

from flask_testing import TestCase

from src import app, db
from src.accounts.models import User
from src.pipelines.models import Pipeline


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        example_user = User(
            username="admin",
            password="admin_user",
            email="ad@min.com",
            role=10,
            created_by="cli",
            last_modified_by="cli",
            is_admin=True,
        )
        db.session.add(example_user)
        example_pipeline = Pipeline(
            name="Example pipeline",
            description="Example pipeline description",
            created_by="cli",
            last_modified_by="cli",
            strategies=[]
        )
        db.session.add(example_pipeline)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        testdb_path = "/opt/40991-TFG-Backend/instance/testdb.sqlite"
        os.remove(testdb_path)
