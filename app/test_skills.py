from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)



####################################### Testing the endpoints in the blacklistemail.py file

def test_get_all_categories():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        "/categories/categories_get_all",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200


def test_post_categories():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.post(
        "/categories/category_post/",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'category_input': 'hola',


        }

    )
    assert response.status_code == 201

    
def test_update_category():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/categories/category_put/hola/hola2"

    response = client.put(
        url=url_input,

    )
    assert response.status_code == 201


def test_delete_category():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    url_input="/categories/category_delete/id/hola2"

    response = client.delete(
        url=url_input,
        
        headers= {"Accept": "*/*",
                 },
    )
    assert response.status_code == 204
