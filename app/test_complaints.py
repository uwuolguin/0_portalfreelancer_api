from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing
import psycopg2
from psycopg2.extras import RealDictCursor
import time



def getConnection():
    

    while True:
        try:

            conn_test_complaint=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_test_complaint




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


def test_post_complaints():

    try:
        SQL_STATEMENT="DELETE FROM public.complaints where created_at = (select max(created_at) from public.complaints where email ='"+settings.cloud_platform_user_for_email_sending+"') AND email = '"+settings.cloud_platform_user_for_email_sending+"';"
        
        print(SQL_STATEMENT)

        conn_test=getConnection()
        cursor=conn_test.cursor()

        cursor.execute(SQL_STATEMENT)

        conn_test.commit()
        conn_test.close()
    except:
        pass

    login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_sending)

    client.cookies={"login": login_cookie}

    response = client.post(
        url="https://apiportalfreelancer.lat/complaints/complaint_post/",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'email_sent': 'hola',
               
        }

    )

    assert response.status_code == 201