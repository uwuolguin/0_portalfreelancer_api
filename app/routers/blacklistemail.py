from fastapi import  status, HTTPException, APIRouter,Cookie,Response
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from pydantic.networks import EmailStr

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

@router.delete("/blacklistemail_delete/id/{email_input}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklistemail(email_input:EmailStr, login: str = Cookie(None)):

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
    
    id_2=""" SELECT * FROM get_by_blacklistemail_v2('%s');"""
    cursor.execute(id_2 % (email_input))
    blacklistemail_psql=cursor.fetchone()
    if blacklistemail_psql ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with blacklistemail_psql: {email_input} does not exist")

    delete=""" SELECT * from delete_blacklistemail_v2('%s');"""
    cursor.execute(delete % (str(email_input)))
    conn_blacklistemail.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/blacklistemail_put/{email_input}/{new_email_input}")
def update_blacklistemail(email_input:EmailStr,new_email_input:str, login: str = Cookie(None)):

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
    

    id_2=""" SELECT * FROM get_by_blacklistemail_v2('%s');"""
    cursor.execute(id_2 % (email_input))
    category=cursor.fetchone()
    if category ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {email_input} does not exist")
    
    update=""" SELECT * FROM update_blacklistemail('%s','%s');"""
    cursor.execute(update % (email_input,new_email_input) )
    conn_blacklistemail.commit()
    
    return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 