from app.main import app
from starlette.testclient import TestClient
from app.config import settings
import pytest
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)

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

            ############################ Testing the normal endpoints

@pytest.mark.parametrize("email,password,expected",[

    (settings.superadmin_email,settings.superadmin_password,{"message": "cookie set" }),
    (settings.cloud_platform_user_for_email_password_changes,settings.test_password_cloud,{"message": "cookie set" }),
    (settings.cloud_platform_user_for_email_sending,settings.test_password_api,{"message": "cookie set" }),
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
    

@pytest.mark.parametrize("email",[

    (settings.superadmin_email),
    (settings.cloud_platform_user_for_email_password_changes),
    (settings.cloud_platform_user_for_email_sending),
])
def test_log_out(email):

    login_cookie=create_cookie_token_access_for_testing(email)

    client.cookies={"login": login_cookie}
    
    response = client.delete(
        "/auth/logout",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200
    assert response.json() == {
                                "status": "success"
                              }

