from datetime import datetime
from src import db


class HealthRecord(db.Model):

    __tablename__ = "health_records"

    # Health record specific fields
    # Path to the stored recording
    recording_path = db.Column(db.String, nullable=False)
    # Result of the transcription
    transcription = db.Column(db.String, nullable=False)
    # Final health record (output of the last strategy)
    health_record = db.Column(db.String, unique=False, nullable=False)
    # All the outputs of the strategies run
    processing_outputs = db.Column(db.JSON, nullable=False)
    # Potential parent of a record
    parent_id = db.Column(db.Integer)

    # Additional data
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    last_modified_by = db.Column(db.String, nullable=True)

    def __init__(self, recording_path, transcription, health_record, processing_outputs, parent_id, created_by, last_modified_by):
        self.recording_path = recording_path
        self.transcription = transcription
        self.health_record = health_record
        self.processing_outputs = processing_outputs
        self.parent_id = parent_id

        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.created_by = created_by
        self.last_modified_by = last_modified_by

    def __repr__(self):
        return f"Result: {self.health_record}\nDone by: {self.created_by}"

    def as_dict(self):
        return {
            'recording_path': self.recording_path,
            'transcription': self.transcription,
            'health_record': self.health_record,
            'processing_outputs': self.processing_outputs,
            'parent_id': self.parent_id,

            'id': self.id,
            'created_at': self.created_at.strftime("%Y/%m/%d - %X"),
            'updated_at': self.updated_at.strftime("%Y/%m/%d - %X"),
            'created_by': self.created_by,
            'last_modified_by': self.last_modified_by,
        }
