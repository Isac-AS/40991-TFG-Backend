from datetime import datetime
from src import db


class Strategy(db.Model):

    __tablename__ = "strategies"

    # Pipeline specific fields
    name = db.Column(db.String, nullable=False)
    description =  db.Column(db.String, nullable=False)
    python_file_path =  db.Column(db.String, nullable=False)
    env_path =  db.Column(db.String, nullable=False)
    input_type =  db.Column(db.String, nullable=False)
    output_type =  db.Column(db.String, nullable=False)
    stage =  db.Column(db.String, nullable=False)

    # Additional data
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    last_modified_by = db.Column(db.String, nullable=True)

    def __init__(self, name, description, python_file_path, env_path, input_type, output_type, stage, created_by, last_modified_by):
        self.name = name
        self.description = description
        self.python_file_path = python_file_path
        self.env_path = env_path
        self.input_type = input_type
        self.output_type = output_type
        self.stage = stage

        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.created_by = created_by
        self.last_modified_by = last_modified_by

    def __repr__(self):
        return f"Name: {self.name}\nDone by: {self.created_by}"
    
    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'python_file_path': self.python_file_path,
            'env_path': self.env_path,
            'input_type': self.input_type,
            'output_type': self.output_type,
            'stage': self.stage,

            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'last_modified_by': self.last_modified_by,
        }
