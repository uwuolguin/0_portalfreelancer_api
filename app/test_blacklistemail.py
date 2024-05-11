from app.main import app
from starlette.testclient import TestClient
from app.config import settings
import pytest
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)



####################################### Testing the endpoints in the blacklistemail.py file

def test_get_all_black_list_email():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        "/blacklistemail/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_all_black_list_email_fail():

    login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_password_changes)

    client.cookies={"login": login_cookie}

    response = client.get(
        "/blacklistemail/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 404

def test_post_black_list_email():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

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
    
