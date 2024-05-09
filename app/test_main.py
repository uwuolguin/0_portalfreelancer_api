from app.main import app
from starlette.testclient import TestClient



client = TestClient(app=app)

####################################### Testing the endpoints in the main.py file
def test_front_page():
    response = client.get("/")
    assert response.status_code == 200

def test_purpose_page():
    response = client.get('/purpose_html/')
    assert response.status_code == 200

####################################### Testing the endpoints in the auth.py file
            ############################ Testing the html endpoints
def test_login_page():
    response = client.get('auth/logIn/')
    assert response.status_code == 200

def test_sign_in_router_page():
    response = client.get('auth/SigInRouter/')
    assert response.status_code == 200

def test_settings_url_for_del_up_page():
    response = client.get('auth/settings_url_for_del_up/')
    assert response.status_code == 200



