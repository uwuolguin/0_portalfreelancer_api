from app.main import app
from starlette.testclient import TestClient
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)

####################################### Testing the endpoints in the main.py file
def test_front_page():
    response = client.get("/")
    assert response.status_code == 200

def test_purpose_page():
    response = client.get('/purpose_html/')
    assert response.status_code == 200

