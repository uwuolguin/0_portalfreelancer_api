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
        #development

        # url="/tableau/tableau_create_webhook/?webhookname=delete_test30&webhookUrl=http://127.0.0.1:8000/tableau/tableau_webhook_fail_refresh_destination/&event=ViewDeleted",

        #production

        url="/tableau/tableau_create_webhook/?webhookname=delete_test30&webhookUrl=https://apiportalfreelancer.lat/tableau/tableau_webhook_fail_refresh_destination/&event=ViewDeleted",
        
        headers= {"Accept": "application/json",

                 },

    )
    id_=response.json().split(",")[5].split(":")[1].replace('''"''',"")


    response_test = client.get(
        url="/tableau/tableau_test_webhook/?webhookId="+id_,
        
        headers= {"Accept": "application/json",

                 },

    )

    url_delete="/tableau/tableau_delete_webhook/?webhookId="+id_

    response_delete = client.delete(
        url=url_delete,
        
        headers= {"Accept": "*/*",
                 },
    )


    assert response.status_code == 201
    assert response_test.status_code == 200
    assert response_delete.status_code == 204

############################ Tableau Extensions API ##########################################

def test_create_cars_table_from_xlsx():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.post(

        "/tableau/tableau_cars_from_excel/",
        
    )
    assert response.status_code == 201


def test_get_tableau_extensions_api_html():

    token=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    response = client.get(

        "/tableau/tableau_extension_api_html/?response="+token,
        
    )
    assert response.status_code == 200