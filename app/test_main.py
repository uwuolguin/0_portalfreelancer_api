from app.main import app
from starlette.testclient import TestClient
from app.config import settings
import pytest



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

            ############################ Testing the html endpoints

@pytest.mark.parametrize("email,password,expected",[

    (settings.superadmin_email,settings.superadmin_password,{"message": "cookie set" }),
    ('portalfreelancerlatsecpass@gmail.com','hola',{"message": "cookie set" }),

])
def test_create_login_http_only_cookie(email,password,expected):
    response = client.post(
        "/auth/login_talent_firm",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'email': email ,
               'password': password

        }

    )
    assert response.status_code == 200
    assert response.json() == expected