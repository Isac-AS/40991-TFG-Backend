import json
import pytest
from src.health_records.models import HealthRecord


@pytest.fixture(scope="function")
def test_record(database, app) -> HealthRecord:
    # Record creation
    test_record_output = [{'output': {'output': 'test_output'}}]
    record = HealthRecord(
        recording_path='audio_file_path',
        transcription="test_output",
        health_record="test_output_ehr",
        processing_outputs=test_record_output,
        parent_id=100,
        created_by="test",
        last_modified_by="test"
    )
    # Test record persistence
    with app.app_context():
        database.session.add(record)
        database.session.commit()
    return record


def test_record_retrieval(client, test_record):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Record is created and inserted in the database
    THEN check the recording path and transcription are saved correctly
    """
    # Record retrieval
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["recording_path"] == "audio_file_path"
    assert parsed_retrieval_response[0]["transcription"] == "test_output"


def test_record_update_and_retrieval(client, test_record: HealthRecord, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Record is created, saved and updated
    THEN check the update is correct by checking the retrieval
    """
    # Record retrieval
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["recording_path"] == "audio_file_path"

    # Record modification
    test_record_2 = parsed_retrieval_response[0]
    test_record_2["transcription"] = "test_transcription_output"
    record_modification_response = client.post("/health_records/update", json={
        "healthRecord": test_record_2
    })
    parsed_modification_response = json.loads(
        record_modification_response.data)
    modification_result = parsed_modification_response["result"]
    assert True == modification_result
    assert "test_transcription_output" == parsed_modification_response[
        "healthRecord"]["transcription"]

    # Record retrieval
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["transcription"] == "test_transcription_output"


def test_record_deletion(client, test_record: HealthRecord):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Record is created, saved and deleted
    THEN check the deletion was successfull by checking there are no entries in the table
    """
    # Record retrieval
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["recording_path"] == "audio_file_path"

    # Record deletion
    record_deletion_response = client.post("/health_records/delete", json={
        "id": parsed_retrieval_response[0]["id"]
    })
    parsed_deletion_response = json.loads(record_deletion_response.data)
    deletion_result = parsed_deletion_response["result"]
    assert True == deletion_result

    # Get_all should be an empty list
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) == 0


def test_unsuccessful_record_update(client, test_record: HealthRecord):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Record is updated with a wrong id
    THEN check the answer received from the backend is negative
    """
    # Record retrieval
    record_retrieval_response = client.get("/health_records/get_all")
    parsed_retrieval_response = json.loads(record_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["recording_path"] == "audio_file_path"

    # Record modification
    test_record_2 = parsed_retrieval_response[0]
    test_record_2["transcription"] = "test_transcription_output"
    test_record_2["id"] = 5
    record_modification_response = client.post("/health_records/update", json={
        "healthRecord": test_record_2
    })
    parsed_modification_response = json.loads(
        record_modification_response.data)
    modification_result = parsed_modification_response["result"]
    assert False == modification_result
