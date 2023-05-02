from src.accounts.models import User
from src.pipelines.models import Pipeline


def test_ping(client):
    response = client.get("/api/ping")
    print(response.data)
    assert b'"ping": "pong!"' in response.data


def test_pipeline_creation(client, test_pipeline: Pipeline, login):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created
    THEN check the name and description fields are defined correctly
    """
    response = client.post("/pipelines/create", json={
        "pipeline": test_pipeline.as_dict()
    })
    print(f"\nResponse data:\n{response.data}\n")
    print(f"\nResponse:\n{response}\n")
    assert True in response.data


def test_pipeline_get_all(client, test_pipeline):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Pipeline is created
    THEN check the name and description fields are defined correctly
    """
    response = client.post("/pipelines/get_all")
    print(f"\nResponse data:\n{response.data}\n")
    assert response.status_code == 405
