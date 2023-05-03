import json
import pytest
from src.strategies.models import Strategy


@pytest.fixture(scope="function")
def test_strategy(database, app) -> Strategy:
    strategy = Strategy(
        name="test_strategy",
        description="test_strategy_description",
        stage="Voz a texto",
        python_file_path="example_python_path",
        env_path="example_env_path",
        input_type="string",
        output_type="string",
        created_by="test",
        last_modified_by="test"
    )
    with app.app_context():
        database.session.add(strategy)
        database.session.commit()
    return strategy


def test_strategy_retrieval(client, test_strategy):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Strategy is created and inserted in the database
    THEN check the name and description fields are defined correctly
    """
    # Strategy retrieval
    strategy_retrieval_response = client.get("/strategies/get_all")
    parsed_retrieval_response = json.loads(strategy_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["name"] == "test_strategy"


def test_strategy_update_and_retrieval(client, test_strategy: Strategy, register):
    """
    GIVEN a Flask application configured for testing
    WHEN a new Strategy is created, saved and updated
    THEN check the update is correct by checking the retrieval
    """
    # Strategy retrieval
    strategy_retrieval_response = client.get("/strategies/get_all")
    parsed_retrieval_response = json.loads(strategy_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["name"] == "test_strategy"

    # Strategy modification
    test_strategy_2 = parsed_retrieval_response[0]
    test_strategy_2["name"] = "test_strategy_2"
    strategy_modification_response = client.post("/strategies/update", json={
        "strategy": test_strategy_2
    })
    parsed_modification_response = json.loads(
        strategy_modification_response.data)
    modification_result = parsed_modification_response["result"]
    assert True == modification_result
    assert "test_strategy_2" == parsed_modification_response["strategy"]["name"]

    # Strategy retrieval
    strategy_retrieval_response = client.get("/strategies/get_all")
    parsed_retrieval_response = json.loads(strategy_retrieval_response.data)
    assert len(parsed_retrieval_response) > 0
    assert parsed_retrieval_response[0]["name"] == "test_strategy_2"
