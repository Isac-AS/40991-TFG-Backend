from datetime import datetime
from src import db


class Pipeline(db.Model):

    __tablename__ = "pipelines"

    # Pipeline specific fields
    name = db.Column(db.String, nullable=False)
    description =  db.Column(db.String, nullable=False)
    strategies = db.Column(db.JSON, nullable=False)

    # Additional data
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    last_modified_by = db.Column(db.String, nullable=True)

    def __init__(self, name, description, strategies, created_by, last_modified_by):
        self.name = name
        self.description = description
        self.strategies = strategies

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
            'strategies': self.strategies,

            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'last_modified_by': self.last_modified_by,
        }
