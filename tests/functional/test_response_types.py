def test_ping(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a ping is sent via HTTP GET
    THEN check the "pong" is received correctly as well as the status code
    """
    response = client.get("/api/ping")
    assert b'"ping": "pong!"' in response.data
    assert response.status_code == 200


def test_blueprint_ping_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a ping is sent via HTTP GET to a blueprint method
    THEN check the "pong" is received correctly
    """
    response = client.get("/api/test")
    assert b'"ping": "pong!"' in response.data
    assert response.status_code == 200


def test_blueprint_ping_post(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a ping is sent via HTTP POST to a blueprint method
    THEN check the "pong" is receive correctly
    """
    response = client.post("/api/test")
    assert b'"ping": "pong!"' in response.data
    assert response.status_code == 200


def test_ping_response(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a ping is sent via HTTP POST and only GET is allowed
    THEN check the status code of the response is 405
    """
    response = client.post("/api/test/get")
    assert response.status_code == 405
