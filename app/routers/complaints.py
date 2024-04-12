from fastapi import  status, HTTPException,APIRouter,Form,Cookie,Request
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



def getConnection():
    

    while True:
        try:

            conn_complaints=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_complaints

router= APIRouter(
    
    prefix="/complaints",
    tags=["Complaints"]
)



@router.get("/complaints_get_all",response_model=list[schemas.complaintResponse])
def get_all_firm(login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_complaints=getConnection()
    cursor=conn_complaints.cursor()

    if login==None:
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_issues+""" """)
    complaint=cursor.fetchall()
    if not complaint :
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    conn_complaints.close()
    return complaint 



@router.post("/complaint_post/",status_code=status.HTTP_201_CREATED)
def post_firm(email_sent:Annotated[str,BeforeValidator(schemas.check_long_str_1000),Form()],login: str = Cookie(None))-> Any:

    email_sent=email_sent.replace("'","")

    os.chdir(settings.normal_directory)

    conn_complaints=getConnection()
    cursor=conn_complaints.cursor()

    if login==None:
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    
    if dict(credentials).get("role") != "talent" and dict(credentials).get("role") != "firm":
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    if dict(credentials).get("role") == "talent":

        email=dict(credentials).get("talent_email")

    else:

        email=dict(credentials).get("firm_email")


################################ 1 complaint per user per day ###################
    email_2="""  SELECT * from complaint_attemp_1_day('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()
    if not(email_today ==None):
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send 1 complaint per day")

    
#################################500 complaints per day #######################
    cursor.execute(""" SELECT * FROM number_of_complaint_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=500:
        conn_complaints.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 500 complaints per day")
###################CREATE USER#####################################################################
    email_uwu="""SELECT insert_complaints('%s','%s');"""
    cursor.execute(email_uwu % (str(email),str(email_sent)))
    conn_complaints.commit()

################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")

@router.get('/complaints_html/',response_class=HTMLResponse)
def complaints_html(request: Request,login: str = Cookie(None)):

    while True:
        try:

            if login==None:
                    context={'request': request}
                    return templates.TemplateResponse("4_log_in_complaints.html",context)
            try:
                credentials=oath2.decode_access_token(login)

                if dict(credentials).get("role") == "superadmin":
                    login_role_value="superadmin"
                elif dict(credentials).get("role") == "firm":
                    login_role_value="firm"
                else:
                    login_role_value="talent"


            except:
                pass


            context={'request': request,'login_role':login_role_value}
            return templates.TemplateResponse("11_complaints.html",context)
        except:
            time.sleep(1)
            pass