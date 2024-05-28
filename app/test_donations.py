from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing




client = TestClient(app=app)

####################################### Testing the HTML endpoints in the donations.py file

def test_get_donations_html():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="/donations/donations_html/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200


