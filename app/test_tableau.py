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

####################################### Testing the endpoints in the tableau.py file
def test_post_test_delete_webhook_tableau():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.post(
        url="https://apiportalfreelancer.lat/tableau/tableau_create_webhook/?webhookname=delete_test30&webhookUrl=https://apiportalfreelancer.lat/tableau/tableau_webhook_fail_refresh_destination/&event=ViewDeleted",
        
        headers= {"Accept": "application/json",

                 },

    )
    id_=response.json().split(",")[5].split(":")[1].replace('''"''',"")


    response_test = client.get(
        url="https://apiportalfreelancer.lat/tableau/tableau_test_webhook/?webhookId="+id_,
        
        headers= {"Accept": "application/json",

                 },

    )

    url_delete="https://apiportalfreelancer.lat/tableau/tableau_delete_webhook/?webhookId="+id_

    response_delete = client.delete(
        url=url_delete,
        
        headers= {"Accept": "*/*",
                 },
    )


    assert response.status_code == 201
    assert response_test.status_code == 200
    assert response_delete.status_code == 204


