from app.main import app
from starlette.testclient import TestClient
from app.config import settings
from app.utils import create_cookie_token_access_for_testing,hash
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os

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

####################################### Testing the HTML endpoints in the talent.py file

def test_get_talent_signupfirm_html():


    response = client.get(
        url="https://apiportalfreelancer.lat/talent/signUpTalent/",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_talent_deluptalent_html():


        login_cookie=create_cookie_token_access_for_testing(email=settings.cloud_platform_user_for_email_password_changes)

        client.cookies={"login": login_cookie}

        response = client.get(
        url="https://apiportalfreelancer.lat/talent/delUpTalent/",
            
            headers= {"Accept": "application/json",
                    },
        )

        assert response.status_code == 200


####################################### Testing the endpoints in the talent.py file

def test_get_all_talent():

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/talent/talent_get_all",
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_talent_id():

    try:

            conn_test=getConnection()
            cursor=conn_test.cursor()

            SQL_STATEMENT_TALENT_ID="SELECT id FROM public.talent where email ='"+settings.cloud_platform_user_for_email_password_changes+"';"   

            cursor.execute(SQL_STATEMENT_TALENT_ID)
            id_talent=cursor.fetchone().get("id")

            conn_test.close()
    except:
            pass

    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/talent/talent_get_id/id/"+str(id_talent),
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_get_talent_email():

    
    login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

    client.cookies={"login": login_cookie}

    response = client.get(
        url="https://apiportalfreelancer.lat/talent/email_validated_2/"+settings.cloud_platform_user_for_email_password_changes,
        
        headers= {"Accept": "application/json",
                 },

    )
    assert response.status_code == 200

def test_post_update_delete_talent():

    ###POST

    os.chdir(settings.picture_directory)

    picture=open('example2.png', 'rb')

    response_post = client.post(
        "/talent/talent_post/",
        

        data= {
            'email': 'delete_for_testing_talent@gmail.com',
            'password':'test',
            'full_name':'test',
            'profession':'test',
            'rate':123,
            'description':'test',
            'linkedin':'https://linkedin.com/',
            'github':'https://github.com/',
            'instagram':'https://instagram.com/',
            'facebook':'https://facebook.com/',
            'skills':'test',
            'categories':'test',

        },

        files={'file': picture}

    )
    
    picture.close()

    os.chdir(settings.normal_directory)

    login_cookie=create_cookie_token_access_for_testing(email="delete_for_testing_talent@gmail.com")

    client.cookies={"login": login_cookie}

    response_put = client.put(
         
        "/talent/talent_put/",
        
        data= {

            'password':'test',
            'full_name':'test_talent_changed',
            'profession':'test',
            'rate':123,
            'description':'test',
            'linkedin':'https://linkedin.com/',
            'github':'https://github.com/',
            'instagram':'https://instagram.com/',
            'facebook':'https://facebook.com/',
            'skills':'test',
            'categories':'test',

        },

    )

    assert response_post.status_code == 201
    assert response_put.status_code == 201
    

#     ####PUT
    
#     login_cookie=create_cookie_token_access_for_testing(email="delete_for_testing@gmail.com")

#     print("login cookie: "+login_cookie)

#     client.cookies={"login": login_cookie}

#     url_input="https://apiportalfreelancer.lat/firm/firm_put/"

#     response_put = client.put(
         
#         url=url_input,

#         headers= {"Accept": "application/json",
#                   "Content-Type": "application/x-www-form-urlencoded"
#                  },
#         data= {'password':'test',
#                'full_name':'test_has_changed',
#                'contact_email':'delete_for_testing@gmail.com',
#                'contact_phone':123456789,
#                'email_template_to_send':'test',
#                'linkedin':'https://linkedin.com/',
#                'instagram':'https://instagram.com/',


#         }

#     )
#     assert response_put.status_code == 201

#     ######DELETE
#     response_delete = client.delete(
#         url="https://apiportalfreelancer.lat/firm/firm_delete/id/",
        
#         headers= {"Accept": "*/*",
#                  },
#     )
#     assert response_delete.status_code == 204


# def test_delete_firm_by_admin():

#     ###POST
    
#     response_post = client.post(
#         "https://apiportalfreelancer.lat/firm/firm_post/",
        
#         headers= {"Accept": "application/json",
#                   "Content-Type": "application/x-www-form-urlencoded"
#                  },
#         data= {'email': 'delete_for_testing_admin@gmail.com',
#                'password':'test',
#                'full_name':'test',
#                'contact_email':'delete_for_testing@gmail.com',
#                'contact_phone':123456789,
#                'email_template_to_send':'test',
#                'linkedin':'https://linkedin.com/',
#                'instagram':'https://instagram.com/',

#         }

#     )
#     assert response_post.status_code == 201

#     try:

#             conn_test=getConnection()
#             cursor=conn_test.cursor()

#             SQL_STATEMENT_FIRM_ID="SELECT id FROM public.firm where email ='delete_for_testing_admin@gmail.com';" 

#             cursor.execute(SQL_STATEMENT_FIRM_ID)

#             id_firm=cursor.fetchone().get("id")

#             conn_test.close()
#     except:
#             pass
#     login_cookie=create_cookie_token_access_for_testing(email=settings.superadmin_email)

#     client.cookies={"login": login_cookie}

#     response_delete = client.delete(
#         url="https://apiportalfreelancer.lat/firm/firm_delete_by_admin/id/"+str(id_firm),
        
#         headers= {"Accept": "*/*",
#                  },
#     )
#     assert response_delete.status_code == 204