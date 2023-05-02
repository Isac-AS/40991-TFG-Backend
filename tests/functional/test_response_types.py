def test_ping(client):
    response = client.get("/api/ping")
    print(response.data)
    assert b'"ping": "pong!"' in response.data

def test_ping_response(client):
    response = client.post("/api/ping")
    assert response.status_code == 405
    
