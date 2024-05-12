from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)



####################################### Testing the endpoints in the blacklistemail.py file

def test_get_all_black_list_word():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        "/blacklistwords/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_all_black_list_word_fail():

    login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_password_changes)

    client.cookies={"login": login_cookie}

    response = client.get(
        "/blacklistwords/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 404

def test_post_black_list_word():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.post(
        "/blacklistwords/",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'words': 'megustaelpeneconsemen',


        }

    )
    assert response.status_code == 201
    assert response.json() ==  ['Black Listed Word Added']
    
def test_update_black_word():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/blacklistwords/blacklistword_put/megustaelpeneconsemen/megustaelpeneconsemen2"

    response = client.put(
        url=url_input,

    )
    assert response.status_code == 201

def test_delete_black_list_word():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/blacklistwords/blacklistword_delete/id/megustaelpeneconsemen2"

    response = client.delete(
        url=url_input,
        
        headers= {"Accept": "*/*",
                 },
    )
    assert response.status_code == 204
