from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)



####################################### Testing the HTML endpoints in the tableau.py file

def test_get_main_tableau_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(

        "/tableau/tableau_html_panel/",
        
    )
    assert response.status_code == 200


def test_get_datasource_tableau_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(

        "/tableau/tableau_html_query_all_datasources/",
        
    )
    assert response.status_code == 200

def test_get_webhook_tableau_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(

        "/tableau/tableau_list_webhooks/",
        
    )
    assert response.status_code == 200

# def test_post_categories():

#     login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

#     client.cookies={"login": login_cookie}

#     response = client.post(
#         "/categories/category_post/",
        
#         headers= {"Accept": "application/json",
#                   "Content-Type": "application/x-www-form-urlencoded"
#                  },
#         data= {'category_input': 'hola',


#         }

#     )
#     assert response.status_code == 201

    
# def test_update_category():

#     login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

#     client.cookies={"login": login_cookie}

#     url_input="/categories/category_put/hola/hola2"

#     response = client.put(
#         url=url_input,

#     )
#     assert response.status_code == 201


# def test_delete_category():

#     login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

#     client.cookies={"login": login_cookie}

#     url_input="/categories/category_delete/id/hola2"

#     response = client.delete(
#         url=url_input,
        
#         headers= {"Accept": "*/*",
#                  },
#     )
#     assert response.status_code == 204
####################################### Testing the normal endpoints in the tableau.py file