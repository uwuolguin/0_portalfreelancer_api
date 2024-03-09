from fastapi import  status, HTTPException,APIRouter,Form,Cookie
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

while True:
    try:

        conn_complaints=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_complaints.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)


router= APIRouter(
    
    prefix="/complaints",
    tags=["Complaints"]
)



@router.get("/complaints_get_all",response_model=list[schemas.complaintResponse])
def get_all_firm(login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_complaints.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_issues+""" """)
    complaint=cursor.fetchall()
    if not complaint :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    return complaint 



@router.post("/complaint_post/",status_code=status.HTTP_201_CREATED)
def post_firm(email_sent:Annotated[str,BeforeValidator(schemas.check_long_str_1000),Form()],login: str = Cookie(None))-> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_complaints.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    
    if dict(credentials).get("role") != "talent" and dict(credentials).get("role") != "firm":
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send 1 complaint per day")

    
#################################500 complaints per day #######################
    cursor.execute(""" SELECT * FROM number_of_complaint_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 500 complaints per day")
###################CREATE USER#####################################################################
    email_uwu="""SELECT insert_complaints('%s','%s');"""
    cursor.execute(email_uwu % (str(email),str(email_sent)))
    conn_complaints.commit()

