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

def getConnection():
    

    while True:
        try:

            conn_blacklistword=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_blacklistword



@router.get("/",response_model=list[schemas.blacklistwordsResponse])
def get_all_blacklistwords(login: str = Cookie(None)) -> Any:
    
    os.chdir(settings.normal_directory)

    conn_blacklistwords=getConnection()
    cursor=conn_blacklistwords.cursor()



    if login==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    cursor.execute(""" SELECT * FROM blacklistwords """)
    words=cursor.fetchall()
    if not words :
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    
    conn_blacklistwords.close()
    return words



@router.post("/",status_code=status.HTTP_201_CREATED)
def post_blacklistwords(words:Annotated[str,Form()],login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_blacklistwords=getConnection()
    cursor=conn_blacklistwords.cursor()


    if login==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")


    words=words.replace(" ", "").lower()
    words_2="""  SELECT insert_blacklistwords('%s');"""
    cursor.execute(words_2 % (words))
    conn_blacklistwords.commit()

    conn_blacklistwords.close()
    return {'Black Listed Word Added'}



@router.delete("/blacklistword_delete/id/{word_input}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklistword(word_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    conn_blacklistwords=getConnection()
    cursor=conn_blacklistwords.cursor()


    if login==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id_2=""" SELECT * FROM get_by_blacklistword_v2('%s');"""
    cursor.execute(id_2 % (word_input))
    blacklistword_psql=cursor.fetchone()
    if blacklistword_psql ==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with blacklistword_psql: {word_input} does not exist")

    delete=""" SELECT * from delete_blacklistword_v2('%s');"""
    cursor.execute(delete % (str(word_input)))
    conn_blacklistwords.commit()

    conn_blacklistwords.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/blacklistword_put/{word_input}/{new_word_input}")
def update_blacklistword(word_input:str,new_word_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    conn_blacklistwords=getConnection()
    cursor=conn_blacklistwords.cursor()

    if login==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    word_input=word_input.replace(" ", "").lower()
    new_word_input=new_word_input.replace(" ", "").lower()


    id_2=""" SELECT * FROM get_by_blacklistword_v2('%s');"""
    cursor.execute(id_2 % (word_input))
    category=cursor.fetchone()
    if category ==None:
        conn_blacklistwords.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {word_input} does not exist")
    
    update=""" SELECT * FROM update_blacklistword('%s','%s');"""
    cursor.execute(update % (word_input,new_word_input) )
    conn_blacklistwords.commit()
    
    conn_blacklistwords.close()
    return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 