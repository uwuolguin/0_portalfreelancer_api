from fastapi import  status, HTTPException, APIRouter,Cookie
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os

router= APIRouter(
    
    prefix="/blacklistemail",
    tags=["Blacklistemail"]
)

while True:
    try:

        conn_blacklistemail=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_blacklistemail.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)

@router.get("/",response_model=list[schemas.blacklistemailResponse])
def get_all_blacklistemail(login: str = Cookie(None)) -> Any:
    os.chdir(settings.normal_directory)
    try:
        conn_blacklistemail.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    cursor.execute(""" SELECT * FROM blacklistemail """)
    mail=cursor.fetchall()
    if not mail :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")

    return mail



@router.post("/",status_code=status.HTTP_201_CREATED)
def post_blacklistemail(email:schemas.email_html,login: str = Cookie(None)) -> Any:
    os.chdir(settings.normal_directory)
    try:
        conn_blacklistemail.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    email=email.replace(" ", "").lower()
    email_2="""  SELECT insert_blacklistemail('%s');"""
    cursor.execute(email_2 % (email))
    conn_blacklistemail.commit()


    return {'Black Listed Email Added'}



