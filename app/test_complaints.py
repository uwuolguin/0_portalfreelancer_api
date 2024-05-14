from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing


client = TestClient(app=app)



####################################### Testing the HTML endpoints in the complaints.py file

def test_get_complaints_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/complaints/complaints_html/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200


####################################### Testing the endpoints in the complaints.py file
def test_get_all_complaints():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/complaints/complaints_get_all",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200
