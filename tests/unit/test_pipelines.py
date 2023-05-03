import json
import pytest
from src.pipelines.models import Pipeline


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


def test_pipeline_creation(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created
    THEN check the name and description fields are defined correctly
    """
    response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_response = json.loads(response.data)
    result = parsed_response["result"]
    response_pipeline = parsed_response["pipeline"]
    assert True == result
    assert response_pipeline["name"] == "test_pipeline"


def test_pipeline_creation_and_retrieval(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created and retrieved
    THEN check the get_all route responds with only one pipeline and check its integrity
    """
    pipeline_creation_response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_creation_response = json.loads(pipeline_creation_response.data)
    result = parsed_creation_response["result"]
    assert True == result

    # Pipeline retrieval
    pipeline_retrieval_response = client.get("/pipelines/get_all")
    parsed_retrieval_response = json.loads(pipeline_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["name"] == "test_pipeline"


def test_pipeline_update_and_retrieval(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created, saved and updated
    THEN check the update is correct by checking the retrieval
    """
    pipeline_creation_response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_creation_response = json.loads(pipeline_creation_response.data)
    creation_result = parsed_creation_response["result"]
    assert True == creation_result

    # Pipeline modification
    test_pipeline_2 = parsed_creation_response["pipeline"]
    test_pipeline_2["name"] = "test_pipeline_2"
    pipeline_modification_response = client.post("/pipelines/update", json={
        "pipeline": test_pipeline_2
    })
    parsed_modification_response = json.loads(
        pipeline_modification_response.data)
    modification_result = parsed_modification_response["result"]
    assert True == modification_result
    assert "test_pipeline_2" == parsed_modification_response["pipeline"]["name"]

    # Pipeline retrieval
    pipeline_retrieval_response = client.get("/pipelines/get_all")
    parsed_retrieval_response = json.loads(pipeline_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["name"] == "test_pipeline_2"


def test_pipeline_deletion(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created, saved and deleted
    THEN check the deletion was successfull by checking there are no entries in the table
    """
    pipeline_creation_response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_creation_response = json.loads(pipeline_creation_response.data)
    creation_result = parsed_creation_response["result"]
    assert True == creation_result

    # Pipeline deletion
    pipeline_deletion_response = client.post("/pipelines/delete", json={
        "id": parsed_creation_response["pipeline"]["id"]
    })
    parsed_deletion_response = json.loads(pipeline_deletion_response.data)
    deletion_result = parsed_deletion_response["result"]
    assert True == deletion_result

    # Get_all should be an empty list
    pipeline_retrieval_response = client.get("/pipelines/get_all")
    parsed_retrieval_response = json.loads(pipeline_retrieval_response.data)
    assert len(parsed_retrieval_response) == 0


def test_unsuccessful_pipeline_creation(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created with the same name as an already existing pipeline
    THEN check the answer received from the backend is negative
    """
    client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_response = json.loads(response.data)
    result = parsed_response["result"]
    assert False == result


def test_unsuccessful_pipeline_update(client, test_pipeline: Pipeline, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is updated with a wrong id
    THEN check the answer received from the backend is negative
    """
    pipeline_creation_response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    parsed_creation_response = json.loads(pipeline_creation_response.data)
    creation_result = parsed_creation_response["result"]
    assert True == creation_result

    # Pipeline modification
    test_pipeline_2 = parsed_creation_response["pipeline"]
    test_pipeline_2["name"] = "test_pipeline_2"
    test_pipeline_2["id"] = 5
    pipeline_modification_response = client.post("/pipelines/update", json={
        "pipeline": test_pipeline_2
    })
    parsed_modification_response = json.loads(
        pipeline_modification_response.data)
    modification_result = parsed_modification_response["result"]
    assert False == modification_result
