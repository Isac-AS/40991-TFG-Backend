

def test_ping(client):
    response = client.get("/api/ping")
    print(response.data)
    assert b'"ping": "pong!"' in response.data
