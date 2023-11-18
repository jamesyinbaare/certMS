from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)


def test_root():
    data = {"Hello": "World"}
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == data
