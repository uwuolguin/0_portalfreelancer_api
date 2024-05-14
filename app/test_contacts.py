from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing



client = TestClient(app=app)

####################################### Testing the HTML endpoints in the contacts.py file

def test_get_contacts_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/contacts/contacts_normal/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200


####################################### Testing the endpoints in the contacts.py file
def test_get_all_contacts():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/contacts/contacts_get_all",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_contacts_talent_id():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/contacts/contact_get_id/id_talent/39",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_contacts_talent_firm_id():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/contacts/contact_get_id/id_talent_firm/39/17",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200


