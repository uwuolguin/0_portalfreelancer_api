from app.main import app
from starlette.testclient import TestClient
from app.config import settings
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
        "/blacklistemail/",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'email': 'correo_para_trolear_lpm_5@gmail.com',


        }

    )
    assert response.status_code == 201
    assert response.json() ==  ["Black Listed Email Added"]
    
def test_update_black_list_email():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/blacklistemail/blacklistemail_put/correo_para_trolear_lpm_5@gmail.com/correo_para_trolear_lpm_6@gmail.com"

    response = client.put(
        url=url_input,

    )
    assert response.status_code == 201

def test_delete_black_list_email():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/blacklistemail/blacklistemail_delete/id/correo_para_trolear_lpm_6@gmail.com"

    response = client.delete(
        url=url_input,
        
        headers= {"Accept": "*/*",
                 },
    )
    assert response.status_code == 204
