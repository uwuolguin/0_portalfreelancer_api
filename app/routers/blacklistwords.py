from fastapi import  status, HTTPException,APIRouter,Form,Cookie,Response
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated


router= APIRouter(
    
    prefix="/blacklistwords",
    tags=["Blacklistwords"]
)

while True:
    try:

        conn_blacklistwords=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_blacklistwords.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)

@router.get("/",response_model=list[schemas.blacklistwordsResponse])
def get_all_blacklistwords(login: str = Cookie(None)) -> Any:
    os.chdir(settings.normal_directory)
    try:
        conn_blacklistwords.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    cursor.execute(""" SELECT * FROM blacklistwords """)
    words=cursor.fetchall()
    if not words :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")

    return words



@router.post("/",status_code=status.HTTP_201_CREATED)
def post_blacklistwords(words:Annotated[str,Form()],login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_blacklistwords.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")


    words=words.replace(" ", "").lower()
    words_2="""  SELECT insert_blacklistwords('%s');"""
    cursor.execute(words_2 % (words))
    conn_blacklistwords.commit()


    return {'Black Listed Word Added'}



@router.delete("/blacklistword_delete/id/{word_input}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklistword(word_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    try:
        conn_blacklistwords.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id_2=""" SELECT * FROM get_by_blacklistword_v2('%s');"""
    cursor.execute(id_2 % (word_input))
    blacklistword_psql=cursor.fetchone()
    if blacklistword_psql ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with blacklistword_psql: {word_input} does not exist")

    delete=""" SELECT * from delete_blacklistword_v2('%s');"""
    cursor.execute(delete % (str(word_input)))
    conn_blacklistwords.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.put("/blacklistemail_put/{email_input}/{new_email_input}")
# def update_blacklistemail(email_input:EmailStr,new_email_input:str, login: str = Cookie(None)):

#     os.chdir(settings.normal_directory)
    
#     try:
#         conn_blacklistwords.rollback()
#     except:
#         pass

#     if login==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
#     credentials=oath2.decode_access_token(login)

#     if dict(credentials).get("role") != "superadmin":
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    

#     id_2=""" SELECT * FROM get_by_blacklistemail_v2('%s');"""
#     cursor.execute(id_2 % (email_input))
#     category=cursor.fetchone()
#     if category ==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {email_input} does not exist")
    
#     update=""" SELECT * FROM update_blacklistemail('%s','%s');"""
#     cursor.execute(update % (email_input,new_email_input) )
#     conn_blacklistwords.commit()
    
#     return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 