from app.main import app
from starlette.testclient import TestClient

client = TestClient(app=app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
