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
    print(f"\nResponse data:\n{response.data}\n")
    parsed_response = json.loads(response.data)
    print(f"\nParsed response:\n{parsed_response}\n")
    result = parsed_response["result"]
    assert True == result

