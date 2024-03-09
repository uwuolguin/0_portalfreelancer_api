from fastapi import  status, HTTPException, APIRouter, Response,Form,Cookie
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

router= APIRouter(
    
    prefix="/categories",
    tags=["Categories"]
)

while True:
    try:

        conn_categories=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_categories.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)

@router.get("/categories_get_all",response_model=list[schemas.categoryResponse])
def get_all_categories() -> Any:

    os.chdir(settings.normal_directory)

    try:
        conn_categories.rollback()
    except:
        pass

    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_categories+""" """)
    category=cursor.fetchall()
    if not category :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    return category


@router.post("/category_post/",status_code=status.HTTP_201_CREATED)
def post_category(

                category_input:Annotated[str,BeforeValidator(schemas.check_long_str_1000),Form()],

                login: str = Cookie(None))-> Any:

    os.chdir(settings.normal_directory)
    
    try:
        conn_categories.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
   
###################CREATE USER#####################################################################

    category_2="""  SELECT insert_category('%s');"""
    cursor.execute(category_2 % (category_input))
    conn_categories.commit()

@router.delete("/category_delete/id/{category_input}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    try:
        conn_categories.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id_2=""" SELECT * FROM get_by_category('%s');"""
    cursor.execute(id_2 % (category_input))
    category=cursor.fetchone()
    if category ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {category_input} does not exist")

    delete=""" SELECT * from delete_category('%s');"""
    cursor.execute(delete % (str(category_input)))
    conn_categories.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/category_put/{category_input}/{new_category_input}")
def update_firm(category_input:str,new_category_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    try:
        conn_categories.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    

    id_2=""" SELECT * FROM get_by_category('%s');"""
    cursor.execute(id_2 % (category_input))
    category=cursor.fetchone()
    if category ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {category_input} does not exist")
    
    update=""" SELECT * FROM update_category('%s','%s');"""
    cursor.execute(update % (category_input,new_category_input) )
    conn_categories.commit()
    
    return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 


