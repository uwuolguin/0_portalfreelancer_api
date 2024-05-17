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

####################################### Testing the HTML endpoints in the firm.py file

def test_get_firm_signupfirm_html():


    response = client.get(
        url="https://apiportalfreelancer.lat/firm/signUpFirm/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_firm_delupfirm_html():


        login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_sending)

        client.cookies={"login": login_cookie}

        response = client.get(
        url="https://apiportalfreelancer.lat/firm/delUpFirm/",
            
            headers= {"Accept": "application/json",
                    },
        )

        assert response.status_code == 200


####################################### Testing the endpoints in the firm.py file

def test_get_all_firm():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/firm/firm_get_all",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_firm_id():

    try:

            conn_test=getConnection()
            cursor=conn_test.cursor()

            SQL_STATEMENT_FIRM_ID="SELECT id FROM public.firm where email ='"+settings.cloud_platform_user_for_email_sending+"';" 

            cursor.execute(SQL_STATEMENT_FIRM_ID)

            id_firm=cursor.fetchone().get("id")

            conn_test.close()
    except:
            pass

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/firm/firm_get_id/id/"+str(id_firm),
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_firm_email():

    
    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/firm/firm_email_validated_2/"+settings.cloud_platform_user_for_email_sending,
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_post_update_delete_firm():

    response_post = client.post(
        "https://apiportalfreelancer.lat/firm/firm_post/",
        
        headers= {"Accept": "application/json",
                  "Content-Type": "application/x-www-form-urlencoded"
                 },
        data= {'email': 'delete_for_testing@gmail.com',
               'password':'test',
               'full_name':'test',
               'contact_email':'delete_for_testing@gmail.com',
               'contact_phone':123456789,
               'email_template_to_send':'test',
               'linkedin':'https://linkedin.com/',
               'instagram':'https://instagram.com/',


        }

    )
    assert response_post.status_code == 201
#         conn_test=getConnection()
#         cursor=conn_test.cursor()
        
#         SQL_STATEMENT="DELETE FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part1' and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"') and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"';"
        
#         cursor.execute(SQL_STATEMENT)

#         conn_test.commit()
#         conn_test.close()

        

#         response_p1 = client.post(
#             "/changepassword/changepassword_part1",
            
#             headers= {"Accept": "application/json",
#                     "Content-Type": "application/x-www-form-urlencoded"
#                     },
#             data= {'email': settings.cloud_platform_user_for_email_sending,


#             }

#         )

#         try:

#             conn_test=getConnection()
#             cursor=conn_test.cursor()

#             SQL_STATEMENT_FIRM_PASSWORD="SELECT PASSWORD FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part1' and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"') and origin='part1' and email='"+settings.cloud_platform_user_for_email_sending+"';"


#             cursor.execute(SQL_STATEMENT_FIRM_PASSWORD)
#             password_firm=cursor.fetchone().get("password")

#             conn_test.commit()
#             conn_test.close()
        
        
#         except:
#             pass

#         try:
#             conn_test=getConnection()
#             cursor=conn_test.cursor()
            
#             SQL_STATEMENT='''DELETE FROM public.changepassword where created_at = (select max(created_at) from public.changepassword where origin='part2') and origin='part2' and email='''+"'"+settings.cloud_platform_user_for_email_sending+"'"+''';'''
            
#             cursor.execute(SQL_STATEMENT)
#             conn_test.commit()
#             conn_test.close()
#         except:
#              pass
        

#         response_p2 = client.post(
#             "/changepassword/changepassword_part2",
            
#             headers= {"Accept": "application/json",
#                     "Content-Type": "application/x-www-form-urlencoded"
#                     },
#             data= {'email': settings.cloud_platform_user_for_email_sending,
#                    'password':password_firm


#             }

#         )


#         try:
#             conn_test=getConnection()
#             cursor=conn_test.cursor()
            
#             password_mod=hash(settings.test_password_api).decode('utf-8')

#             SQL_STATEMENT="UPDATE public.firm SET password = '"+password_mod+"' WHERE email = '"+settings.cloud_platform_user_for_email_sending+"';"
            
#             cursor.execute(SQL_STATEMENT)


#             conn_test.commit()
#             conn_test.close()
#         except:
#              pass
        
#         assert response_p1.status_code == 200
#         assert response_p2.status_code == 200


