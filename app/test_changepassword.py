from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing,hash
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

def test_get_changepassword_p1_html():


    response = client.get(
        url="/changepassword/changePasswordP1/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_changepassword_p2_html():


    response = client.get(
        url="/changepassword/changePasswordP2/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200
####################################### Testing the endpoints in the contacts.py file


def test_post_changepassword_p1_p2():


        
        conn_test=getConnection()
        cursor=conn_test.cursor()
        
        SQL_STATEMENT="DELETE FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part1' and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"') and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"';"
        
        cursor.execute(SQL_STATEMENT)

        conn_test.commit()
        conn_test.close()

        

        response_p1 = client.post(
            "/changepassword/changepassword_part1",
            
            headers= {"Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
                    },
            data= {'email': settings.cloud_platform_user_for_email_sending,


            }

        )

        try:

            conn_test=getConnection()
            cursor=conn_test.cursor()

            SQL_STATEMENT_FIRM_PASSWORD="SELECT PASSWORD FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part1' and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"') and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"';"


            cursor.execute(SQL_STATEMENT_FIRM_PASSWORD)
            password_firm=cursor.fetchone().get("password")

            conn_test.commit()
            conn_test.close()
        
        
        except:
            pass

        try:
            conn_test=getConnection()
            cursor=conn_test.cursor()
            
            SQL_STATEMENT='''DELETE FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part2') and origin='part2' and email='''+"'"+settings.cloud_platform_user_for_email_sending+"'"+''';'''
            
            cursor.execute(SQL_STATEMENT)
            conn_test.commit()
            conn_test.close()
        except:
             pass
        

        response_p2 = client.post(
            "/changepassword/changepassword_part2",
            
            headers= {"Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
                    },
            data= {'email': settings.cloud_platform_user_for_email_sending,
                   'password':password_firm


            }

        )


        try:
            conn_test=getConnection()
            cursor=conn_test.cursor()
            
            password_mod=hash(settings.test_password_api).decode('utf-8')

            SQL_STATEMENT="UPDATE public.firm SET password = '"+password_mod+"' WHERE email = '"+settings.cloud_platform_user_for_email_sending+"';"
            
            cursor.execute(SQL_STATEMENT)


            conn_test.commit()
            conn_test.close()
        except:
             pass
        
        assert response_p1.status_code == 200
        assert response_p2.status_code == 200


