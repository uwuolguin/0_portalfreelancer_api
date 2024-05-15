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

def test_get_contacts_firm_id():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/contacts/contact_get_id/id_firm/17",
        
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

def test_post_complaints():

        try:

            conn_test=getConnection()
            cursor=conn_test.cursor()

            SQL_STATEMENT_FIRM_ID="SELECT id FROM public.firm where email ='"+settings.cloud_platform_user_for_email_sending+"';"       
            cursor.execute(SQL_STATEMENT_FIRM_ID)
            id_firm=cursor.fetchone().get("id")


            SQL_STATEMENT_TALENT_ID="SELECT id FROM public.talent where email ='"+settings.cloud_platform_user_for_email_password_changes+"';"       
            cursor.execute(SQL_STATEMENT_TALENT_ID)
            id_talent=cursor.fetchone().get("id")

            
            SQL_STATEMENT='''DELETE FROM public.contacts where created_at = (select max(created_at) from public.contacts) and firm_id = '''+str(id_firm) +''' and talent_id= '''+str(id_talent)+''';'''
            
            cursor.execute(SQL_STATEMENT)

            conn_test.commit()
            conn_test.close()
        
        
        except:
            pass

        login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_sending)

        client.cookies={"login": login_cookie}

        response = client.post(
            url="https://apiportalfreelancer.lat/contacts/contacts/post/"+str(id_talent),
            
            headers= {"Accept": "application/json",
                    },
        )

        assert response.status_code == 200

